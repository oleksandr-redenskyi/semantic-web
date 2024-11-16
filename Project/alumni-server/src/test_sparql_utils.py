import unittest
from unittest.mock import patch, MagicMock
from sparql_utils import DBpediaData

class TestDBpediaData(unittest.TestCase):
    def test_sanitize_input(self):
        input_str = "Taras Shevchenko"
        expected_output = "Taras%20Shevchenko"
        self.assertEqual(DBpediaData.sanitize_input(input_str), expected_output)

    def test_parse_property(self):
        # Test empty string
        self.assertIsNone(DBpediaData.parse_property(''))

        # Test single value
        self.assertEqual(DBpediaData.parse_property('value1'), 'value1')

        # Test multiple values
        self.assertEqual(
            DBpediaData.parse_property('value1|value2|value3'),
            ['value1', 'value2', 'value3']
        )

    def test_filter_properties(self):
        data = {
            'wikiPageID': '12345',
            'rdf-schema#label': 'Some label',
            'name': 'John Doe',
            'age': 30,
            'rdf-schema#comment': 'Some comment',
            'wikiPageLength': '2000',
            'occupation': None
        }
        expected_output = {
            'name': 'John Doe',
            'age': 30
        }
        self.assertEqual(DBpediaData.filter_properties(data), expected_output)

    @patch('sparql_utils.SPARQLWrapper')
    def test_get_alumni(self, mock_sparql_wrapper):
        # Mock the SPARQLWrapper instance
        mock_sparql = MagicMock()
        mock_sparql_wrapper.return_value = mock_sparql

        # Mock the response from query().convert()
        mock_sparql.query.return_value.convert.return_value = {
            "results": {
                "bindings": [
                    {
                        "person": {"type": "uri", "value": "http://dbpedia.org/resource/Person1"},
                        "name_sample": {"type": "literal", "value": "Person One"},
                        "alt_names": {"type": "literal", "value": "Person One|Person Uno"}
                    },
                    {
                        "person": {"type": "uri", "value": "http://dbpedia.org/resource/Person2"},
                        "name_sample": {"type": "literal", "value": "Person Two"},
                        "alt_names": {"type": "literal", "value": "Person Two|Person Dos"}
                    }
                ]
            }
        }

        # Call the method
        result = DBpediaData.get_alumni()

        # Expected result
        expected_result = [
            {
                "id": "Person1",
                "name": "Person One",
                "alt_names": ["Person One", "Person Uno"]
            },
            {
                "id": "Person2",
                "name": "Person Two",
                "alt_names": ["Person Two", "Person Dos"]
            }
        ]
        self.assertEqual(result, expected_result)

    @patch('sparql_utils.SPARQLWrapper')
    def test_get_person_data(self, mock_sparql_wrapper):
        # Mock the SPARQLWrapper instance
        mock_sparql = MagicMock()
        mock_sparql_wrapper.return_value = mock_sparql

        # Mock the response from query().convert()
        mock_sparql.query.return_value.convert.return_value = {
            "results": {
                "bindings": [
                    {
                        "property": {"type": "uri", "value": "http://dbpedia.org/ontology/birthDate"},
                        "values": {"type": "literal", "value": "1980-01-01"}
                    },
                    {
                        "property": {"type": "uri", "value": "http://dbpedia.org/ontology/occupation"},
                        "values": {"type": "literal", "value": "Engineer|Scientist"}
                    },
                    {
                        "property": {"type": "uri", "value": "http://dbpedia.org/ontology/wikiPageID"},
                        "values": {"type": "literal", "value": "123456"}
                    },
                    {
                        "property": {"type": "uri", "value": "http://dbpedia.org/ontology/rdf-schema#label"},
                        "values": {"type": "literal", "value": "Label"}
                    },
                    {
                        "property": {"type": "uri", "value": "http://dbpedia.org/ontology/thumbnail"},
                        "values": {"type": "literal", "value": "http://example.com/image.jpg"}
                    }
                ]
            }
        }

        # Call the method
        result = DBpediaData.get_person_data('Person1')

        # Expected result after filtering
        expected_result = {
            'birthDate': '1980-01-01',
            'occupation': ['Engineer', 'Scientist'],
            'thumbnail': 'http://example.com/image.jpg'
        }
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
