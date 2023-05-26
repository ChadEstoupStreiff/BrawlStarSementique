import streamlit as st
from sementic import load_rdf_file, test_query, get_brawlers, get_maps


def test_ui() -> None:
    with st.sidebar:
        submit = st.form("Test").form_submit_button(
            "Test Request", use_container_width=True
        )

    if submit:
        results = test_query()
        st.write(results)
        # for row in results:
        #     subject, predicate, obj = row
        #     st.write(f"{subject}, {predicate}, {obj}")


def map_ui() -> None:
    with st.sidebar:
        map_form = st.form("MapForm")
        map_form.title("Brawler picks")
        map = map_form.selectbox("Map", get_maps())
        submit = map_form.form_submit_button(
            "Search good Brawler", use_container_width=True
        )

    if submit:
        pass


def brawler_ui() -> None:
    with st.sidebar:
        brawler_form = st.form("BrawlerForm")
        brawler_form.title("Map picks")
        brawler = brawler_form.selectbox("Brawler", get_brawlers())
        submit = brawler_form.form_submit_button(
            "Search good Map", use_container_width=True
        )

    if submit:
        pass


def compatibility_ui() -> None:
    with st.sidebar:
        compatibility_form = st.form("CompatiblityForm")
        compatibility_form.title("Map & Brawler compatibility")
        map = compatibility_form.selectbox("Map", get_maps())
        brawler = compatibility_form.selectbox("Brawler", get_brawlers())
        submit = compatibility_form.form_submit_button(
            "See compatibility", use_container_width=True
        )

    if submit:
        pass


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
    test_ui()
    map_ui()
    brawler_ui()
    compatibility_ui()
