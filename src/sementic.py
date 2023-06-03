from typing import List

import streamlit as st
from rdflib import Graph, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery


def _get_subclasses(class_name):
    query_template = """
        SELECT ?subclass
        WHERE {
            ?subclass rdfs:subClassOf* :%s .
        }
    """

    query = prepareQuery(
        query_template % class_name,
        initNs={
            "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "": st.session_state.namespace,
        },
    )

    sub_classes = [
        row.subclass.replace(st.session_state.namespace, "")
        for row in st.session_state.graph.query(query)
    ]
    sub_classes.remove(class_name)
    return sub_classes


def _get_individuals(class_name):
    query_template = """
        SELECT ?individual
        WHERE {
            ?individual rdf:type :%s .
        }
    """

    query = prepareQuery(
        query_template % class_name,
        initNs={
            "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "": st.session_state.namespace,
        },
    )

    return [
        row.individual.replace(st.session_state.namespace, "")
        for row in st.session_state.graph.query(query)
    ]


@st.cache_data
def get_object_properties(individual):
    query_template = f"""
        SELECT ?property ?propertyValue
        WHERE {{
            <{st.session_state.namespace}%s> ?property ?propertyValue .
            FILTER(isIRI(?propertyValue))
        }}
    """

    query = prepareQuery(
        query_template % individual,
        initNs={
            "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "": st.session_state.namespace,
        },
    )

    return [
        [
            row[0]
            .replace(st.session_state.namespace, "")
            .replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
            .replace("http://www.w3.org/2002/07/owl#", ""),
            row[1]
            .replace(st.session_state.namespace, "")
            .replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
            .replace("http://www.w3.org/2002/07/owl#", ""),
        ]
        for row in st.session_state.graph.query(query)
    ]


@st.cache_data
def get_data_properties(individual):
    query_template = f"""
        SELECT ?property ?propertyValue
        WHERE {{
            <{st.session_state.namespace}%s> ?property ?propertyValue .
            FILTER(isLiteral(?propertyValue))
        }}
    """

    query = prepareQuery(
        query_template % individual,
        initNs={
            "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "": st.session_state.namespace,
        },
    )

    return [
        [
            row[0].replace(st.session_state.namespace, ""),
            row[1].replace(st.session_state.namespace, ""),
        ]
        for row in st.session_state.graph.query(query)
    ]


def get_properties(individual):
    properties = get_data_properties(individual)
    properties.extend(get_object_properties(individual))
    return properties


@st.cache_data
def get_brawlers() -> List:
    results = []
    for sub_class in _get_subclasses("brawler"):
        results.extend([f"{sub_class} > {row}" for row in _get_individuals(sub_class)])
    return results


@st.cache_data
def get_maps() -> List:
    results = []
    for sub_class in _get_subclasses("map"):
        results.extend([f"{sub_class} > {row}" for row in _get_individuals(sub_class)])
    return results


def load_rdf_file(data_url: str = "/data/bdd.rdf") -> bool:
    if "graph" not in st.session_state:
        try:
            st.session_state.namespace = (
                "http://www.semanticweb.org/chad/ontologies/2023/4/untitled-ontology-3#"
            )
            st.session_state.graph = Graph()
            st.session_state.graph.parse(data_url)
        except:
            return False
    return True
