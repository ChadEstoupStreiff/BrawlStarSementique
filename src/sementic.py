from typing import List

import streamlit as st
from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery


def _process_results(results) -> List:
    return [[element for element in row] for row in results]


@st.cache_data
def get_brawlers() -> List:

    # # Define the namespace and class name
    # class_name = "YourClassName"

    # # Prepare the SPARQL query template
    # query_template = """
    #     SELECT ?individual
    #     WHERE {
    #         ?individual rdf:type :%s .
    #     }
    # """

    # # Create the complete query
    # query = prepareQuery(query_template % class_name)

    # return _process_results([row[0] for row in st.session_state.graph.query(query)])
    query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
    """
    return _process_results([row[0] for row in st.session_state.graph.query(query)])

@st.cache_data
def get_maps() -> List:
    query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
    """
    return _process_results([row[0] for row in st.session_state.graph.query(query)])

def test_query() -> List:
    query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
    """
    return _process_results(st.session_state.graph.query(query))


def load_rdf_file(data_url: str = "/data/bdd.rdf") -> bool:
    if "graph" not in st.session_state:
        try:
            st.session_state.graph = Graph()
            st.session_state.graph.parse(data_url)
        except:
            return False
    return True
