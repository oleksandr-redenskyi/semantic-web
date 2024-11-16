import os
from typing import Any, Dict, List
import logging
from urllib.parse import quote

from SPARQLWrapper import SPARQLWrapper, JSON


log = logging.getLogger(__name__)


UNIVERSITY_URI = os.getenv('UNIVERSITY_URI', "dbr:Taras_Shevchenko_National_University_of_Kyiv")


class DBpediaData:
    endpoint_url = os.getenv('SPARQL_ENDPOINT_URL', "http://dbpedia.org/sparql")

    @staticmethod
    def sanitize_input(input: str):
        user_input_encoded = quote(input, safe='')
        return user_input_encoded

    @staticmethod
    def parse_property(value: str):
        values = [v for v in value.split('|') if v]
        if len(values) == 0:
            return None

        if len(values) == 1:
            return values[0]

        return values

    @staticmethod
    def filter_properties(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            k:v
            for k,v in data.items()
            if k.find('wiki') == -1  # filter out properties like wikiPageID and wikiPageLength
            and k.find('rdf-schema') == -1  # filter out rdf-schema#comment and rdf-schema#label which are duplicate data
            and v is not None  # filter out empty properties
        }

    @classmethod
    def get_alumni(cls) -> List[Dict[str, Any]]:
        """Returns a list of alumni from Taras Shevchenko Kyiv National University with their names and URIs."""
        sparql = SPARQLWrapper(cls.endpoint_url)
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?person SAMPLE(?name) AS ?name_sample (GROUP_CONCAT(?name_any; separator='|') AS ?alt_names)
        WHERE {{
            ?person dbo:almaMater {UNIVERSITY_URI} .

            OPTIONAL {{
                ?person foaf:name | rdfs:label ?name_en .
                FILTER (lang(?name_en) = 'en')
            }}

            OPTIONAL {{
                ?person foaf:name | rdfs:label ?name_any .
            }}

            BIND (COALESCE(?name_en, ?name_any) AS ?name)
            FILTER(BOUND(?name))
        }}
        GROUP by ?person
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        alumni = []
        for result in results["results"]["bindings"]:
            alumni.append({
                "id": result["person"]["value"].split('http://dbpedia.org/resource/')[-1],
                "name": result["name_sample"]["value"],
                "alt_names": result["alt_names"]["value"].split('|'),
            })
        return alumni

    @classmethod
    def get_person_data(cls, person_id: str) -> Dict[str, Any]:
        """Returns detailed information about a person given their URI."""
        sparql = SPARQLWrapper(cls.endpoint_url)
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?property (GROUP_CONCAT(?value; separator='|') AS ?values)
        WHERE {{
            BIND(<http://dbpedia.org/resource/{cls.sanitize_input(person_id)}> AS ?person)
            ?person ?property ?value .

            # Only return properties the values of which are english strings
            # or non-string types such as int or date
            # This will filter out the properties with iri values
            FILTER(lang(?value) = 'en' || BOUND(datatype(?value)) || ?property = dbo:thumbnail)
        }}
        GROUP BY ?property
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        log.info(f'results: {results}')
        person_data = {}
        for result in results["results"]["bindings"]:
            property_name = result["property"]["value"].split('/')[-1]
            person_data[property_name] = DBpediaData.parse_property(result["values"]["value"])

        person_data = DBpediaData.filter_properties(person_data)
        return person_data
