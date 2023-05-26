import streamlit as st
from sementic import load_rdf_file, get_brawlers, get_maps
from time import sleep

def map_ui() -> None:
    with st.sidebar:
        map_form = st.form("MapForm")
        map_form.title("Brawler picks")
        map = map_form.selectbox("Map", get_maps()).split(" > ")[1]
        submit = map_form.form_submit_button(
            "Search good Brawler", use_container_width=True
        )

    if submit:
        with st.spinner(f"Searching picks for map {map}..."):
            sleep(3)
            st.error("In dev ...")


def brawler_ui() -> None:
    with st.sidebar:
        brawler_form = st.form("BrawlerForm")
        brawler_form.title("Map picks")
        brawler = brawler_form.selectbox("Brawler", get_brawlers()).split(" > ")[1]
        submit = brawler_form.form_submit_button(
            "Search good Map", use_container_width=True
        )

    if submit:
        with st.spinner(f"Searching picks for brawler {brawler}..."):
            sleep(3)
            st.error("In dev ...")


def compatibility_ui() -> None:
    with st.sidebar:
        compatibility_form = st.form("CompatiblityForm")
        compatibility_form.title("Map & Brawler compatibility")
        map = compatibility_form.selectbox("Map", get_maps()).split(" > ")[1]
        brawler = compatibility_form.selectbox("Brawler", get_brawlers()).split(" > ")[1]
        submit = compatibility_form.form_submit_button(
            "See compatibility", use_container_width=True
        )

    if submit:
        with st.spinner(f"Calculating compatibility between map {map} and brawler {brawler} ..."):
            sleep(3)
            st.error("In dev ...")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Web Sementique Ales",
        page_icon="random",
        # layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    # Load BDD
    with st.sidebar:
        with st.spinner("Loading RDF DataBase"):
            if not load_rdf_file():
                st.error("Error loading RDF DataBase !")
                st.stop()
        st.success("RDF DataBase successfully loaded")

    # Display UI
    map_ui()
    brawler_ui()
    compatibility_ui()
