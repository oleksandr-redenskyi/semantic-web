from datetime import datetime
import os
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD, SDO
from rdflib import BNode, Graph, URIRef, Literal, Namespace
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    g = Graph()

    # Shorten outputs
    g.bind("foaf", FOAF)
    g.bind("xsd", XSD)
    g.bind("schema", SDO)
    ex = Namespace('http://example.org')
    g.bind("ex", ex)

    # Кейд живе за адресою 1516 Henry Street, Берклі, Каліфорнія 94709, США.
    caid = URIRef("/person/caid", base=ex)

    caid_address = URIRef("/person/caid/address", base=ex)
    address_props = [
        (RDF.type, SDO.PostalAddress),
        (SDO.addressCountry, Literal("US")),  # ISO 3166-1 alpha-2 country code.
        (SDO.addressLocality, Literal("Берклі", lang='uk')),
        (SDO.addressRegion, Literal("Каліфорнія", lang='uk')),
        (SDO.postalCode, Literal("94709", datatype=XSD.string)),
        (SDO.streetAddress, Literal("1516 Henry Street")),
    ]
    for (pred, obj) in address_props:
        g.add((caid_address, pred, obj))

    g.add((caid, RDF.type, FOAF.Person))
    g.add((caid, FOAF.givenName, Literal("Кейд", lang='uk')))
    g.add((caid, SDO.address, caid_address))

    # Він має ступінь бакалавра біології в Каліфорнійському університеті з 2011 року.
    california_university = URIRef('/university/ucla', base=ex)
    g.add((california_university, RDF.type, SDO.EducationalOrganization))
    g.add((california_university, RDFS.label, Literal("Каліфорнійський університет", lang='uk')))
    caid_degree = URIRef("/person/caid/degree", base=ex)
    g.add((caid_degree, RDF.type, SDO.EducationalOccupationalCredential))
    g.add((caid_degree, SDO.author, caid))
    g.add((caid_degree, SDO.credentialCategory, Literal("degree", datatype=XSD.string)))
    g.add((caid_degree, SDO.educationalLevel, Literal("bachelor", datatype=XSD.string)))
    g.add((caid_degree, SDO.competencyRequired, Literal("biology", datatype=XSD.string)))
    g.add((caid_degree, SDO.recognizedBy, california_university))
    g.add((caid_degree, SDO.datePublished, Literal(2011, datatype=XSD.year)))

    # Його інтереси: птахи, екологія, довкілля, фотографія і подорожі.
    topic_birds = URIRef('/topic/birds', base=ex)
    topic_ecology = URIRef('/topic/ecology', base=ex)
    topic_environment = URIRef('/topic/environment', base=ex)
    topic_photography = URIRef('/topic/photography', base=ex)
    topic_travelling = URIRef('/topic/travelling', base=ex)
    g.add((caid, FOAF.topic_interest, topic_birds))
    g.add((caid, FOAF.topic_interest, topic_ecology))
    g.add((caid, FOAF.topic_interest, topic_environment))
    g.add((caid, FOAF.topic_interest, topic_photography))
    g.add((caid, FOAF.topic_interest, topic_travelling))

    # Він відвідав Канаду та Францію.
    visited_place = URIRef("/actions/visited-place", base=ex)
    g.add((visited_place, RDF.type, RDF.Property))
    g.add((visited_place, RDFS.domain, FOAF.Person))
    g.add((visited_place, RDFS.range, SDO.Place))

    canada = URIRef("/country/canada", base=ex)
    france = URIRef("/country/france", base=ex)
    g.add((canada, RDF.type, SDO.Country))
    g.add((france, RDF.type, SDO.Country))
    g.add((caid, visited_place, canada))
    g.add((caid, visited_place, france))

    # Емма живе за адресою Carrer de la Guardia Civil 20, 46020 Valencia, Spain.
    emma = URIRef("/person/emma", base=ex)
    emma_address = URIRef("/person/emma/address", base=ex)
    address_props = [
        (RDF.type, SDO.PostalAddress),
        (SDO.addressCountry, Literal("ES", datatype=XSD.string)),  # ISO 3166-1 alpha-2 country code.
        (SDO.addressRegion, Literal("Valencia")),
        (SDO.postalCode, Literal("46020", datatype=XSD.string)),
        (SDO.streetAddress, Literal("Carrer de la Guardia Civil 20", lang="es")),
    ]
    for (pred, obj) in address_props:
        g.add((emma_address, pred, obj))

    g.add((emma, RDF.type, FOAF.Person))
    g.add((emma, FOAF.givenName, Literal("Емма", lang="uk")))
    g.add((emma, SDO.address, emma_address))

    # Вона має ступінь магістра хімії в Університеті Валенсії з 2015 року.
    valencia_university = URIRef('/university/uv', base=ex)
    g.add((valencia_university, RDF.type, SDO.EducationalOrganization))
    g.add((valencia_university, RDFS.label, Literal("Університет Валенсії", lang='uk')))
    emma_degree = URIRef("/person/emma/degree", base=ex)
    g.add((emma_degree, RDF.type, SDO.EducationalOccupationalCredential))
    g.add((emma_degree, SDO.author, emma))
    g.add((emma_degree, SDO.credentialCategory, Literal("degree", datatype=XSD.string)))
    g.add((emma_degree, SDO.educationalLevel, Literal("master", datatype=XSD.string)))
    g.add((emma_degree, SDO.competencyRequired, Literal("chemistry", datatype=XSD.string)))
    g.add((emma_degree, SDO.recognizedBy, valencia_university))
    g.add((emma_degree, SDO.datePublished, Literal(2015, datatype=XSD.gYear)))

    # Її сфера знань включає управління відходами , токсичні відходи, забруднення повітря.
    waste_management = URIRef('/topic/waste-management', base=ex)
    toxic_waste = URIRef('/topic/toxic-waste', base=ex)
    air_pollution = URIRef('/topic/air-pollution', base=ex)
    g.add((emma, SDO.knowsAbout, waste_management))
    g.add((emma, SDO.knowsAbout, toxic_waste))
    g.add((emma, SDO.knowsAbout, air_pollution))

    # Її інтереси: їзда на велосипеді, музика та подорожі.
    topic_cycling = URIRef('/topic/cycling', base=ex)
    topic_music = URIRef('/topic/music', base=ex)
    g.add((emma, FOAF.topic_interest, topic_cycling))
    g.add((emma, FOAF.topic_interest, topic_music))
    g.add((emma, FOAF.topic_interest, topic_travelling))

    # Вона відвідала Португалію, Італію, Францію, Німеччину, Данію та Швецію.
    portugal = URIRef("/country/portugal", base=ex)
    italy = URIRef("/country/italy", base=ex)
    germany = URIRef("/country/germany", base=ex)
    denmark = URIRef("/country/denmark", base=ex)
    sweden = URIRef("/country/sweden", base=ex)
    for country in [portugal, italy, germany, denmark, sweden]:
        g.add((country, RDF.type, SDO.Country))
        g.add((emma, visited_place, country))

    g.add((emma, visited_place, france))

    # Кейд знає Емму.
    g.add((caid, FOAF.knows, emma))

    # Вони зустрілися в Парижі в серпні 2014 року.
    paris = URIRef("/city/paris", base=ex)
    g.add((paris, RDF.type, SDO.City))
    meeting = URIRef("/events/caid-and-emma-meeting", base=ex)
    g.add((meeting, RDF.type, SDO.Event))
    bag = BNode()
    g.add((meeting, SDO.attendee, bag))
    g.add((bag, RDF.type, RDF.Bag))
    g.add((bag, RDF._1, emma))
    g.add((bag, RDF._2, caid))
    g.add((meeting, SDO.startDate, Literal("2014-08", datatype=XSD.gYearMonth)))
    g.add((meeting, SDO.location, paris))


    # • використовуючі словники FOAF, RDF, XSD тощо та власні URI (наприклад,
    # створені на базі http://example.org/) створіть RDF граф за допомогою RDFLib;
    # • виконайте візуалізацію та сериалізацію графу у різні формати;
    g.serialize('graph.xml', format='xml', encoding='utf-8')

    g.serialize('graph.nt', format='nt', encoding='utf-8')

    g.serialize('graph.ttl', format='turtle', encoding='utf-8')


    # • запишіть свій граф у файл у форматі TURTLE;
    # • перегляньте файл і відредагуйте його так, щоб Кейд також відвідував Німеччину і
    # щоб Еммі було 36 років;
    if os.path.exists('graph_edited.ttl'):
        print('File "graph_edited.ttl" already exists')
    else:
        g.serialize('graph_edited.ttl', format='turtle')

    # • виведіть на консоль усі трійки графу;
    print('\nAll triples')
    for s, p, o in g:
        print(f'{s} {p} {o}')

    # • виведіть на консоль трійки, що стосуються лише про Емму;
    print('\nTriples containing Emma')
    for s, p, o in g.triples((emma, None, None)):
        print(f'{s} {p} {o}')
    for s, p, o in g.triples((None, None, emma)):
        if s == emma:
            continue
        print(f'{s} {p} {o}')

    # • виведіть на консоль трійки, що містять імена людей.
    print('\nTriples with people names')
    for s, p, o in g.triples((None, FOAF.givenName, None)):
        print(f'{s} {p} {o}')




    G = rdflib_to_networkx_multidigraph(g)
    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, with_labels=True)

    #if not in interactive mode for
    plt.show()
