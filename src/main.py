import streamlit as st
from rdflib import Graph



def _load_rdf_file():
    if "graph" not in st.session_state:
        st.session_state.graph = Graph()    

if __name__ == "__main__":
    st.set_page_config(
        page_title="Web Sementique Ales",
        page_icon="random",
        # layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    with st.spinner("Loading RDF DataBase"):
        _load_rdf_file()
