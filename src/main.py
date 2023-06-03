from time import sleep

import streamlit as st
from sementic import get_brawlers, get_maps, get_properties, load_rdf_file


def map_ui() -> None:
    with st.sidebar:
        map_form = st.form("MapForm")
        map_form.title("Maps")
        map = map_form.selectbox("Map", get_maps()).split(" > ")[1]
        submit_info = map_form.form_submit_button(
            "See map info", use_container_width=True
        )
        submit = map_form.form_submit_button(
            "Search good Brawler", use_container_width=True
        )

    if submit_info:
        with st.spinner(f"Getting info of {map}..."):
            infos = get_properties(map)
        for info in infos:
            if info[0] == "type":
                if info[1] != "NamedIndividual":
                    st.subheader(f"Is type {info[1]}")
            elif info[0] == "hasMapTag":
                st.subheader(f"Has map tag {info[1]}")

    if submit:
        with st.spinner(f"Searching picks for map {map}..."):
            map_tags = get_map_tag(get_properties(map))

            res = []
            for brawler in get_brawlers():
                brawler = brawler.split(" > ")[1]
                compatibility = int(calculate_compatibility(
                    brawler_map_tags=get_map_tag(get_properties(brawler)),
                    map_map_tags=map_tags,
                ) * 100)
                added = False
                if len(res) > 0:
                    for i in range(len(res)):
                        if res[i][0] < compatibility:
                            res.insert(i, [compatibility, brawler])
                            added = True
                            break
                if not added:
                    res.append([compatibility, brawler])

            for row in res:
                st.subheader(f"{row[0]}% with brawler {row[1]}")


def brawler_ui() -> None:
    with st.sidebar:
        brawler_form = st.form("BrawlerForm")
        brawler_form.title("Brawlers")
        brawler = brawler_form.selectbox("Brawler", get_brawlers()).split(" > ")[1]
        submit_info = brawler_form.form_submit_button(
            "See brawler info", use_container_width=True
        )
        submit = brawler_form.form_submit_button(
            "Search good Map", use_container_width=True
        )

    if submit_info:
        with st.spinner(f"Getting info of {brawler}..."):
            infos = get_properties(brawler)
        for info in infos:
            if info[0] == "type":
                if info[1] != "NamedIndividual":
                    st.subheader(f"Is type {info[1]}")
            elif info[0] == "hasMapTag":
                st.subheader(f"Adapted to map with tag {info[1]}")
            elif info[0] == "hasMovingSpeed":
                st.subheader(f"Has moving speed of {info[1]}")
            elif info[0] == "hasRange":
                st.subheader(f"Has range of {info[1]}")
            elif info[0] == "hasReloadSpeed":
                st.subheader(f"Has reload speed of {info[1]}")
            elif info[0] == "damage":
                st.subheader(f"Has damage of {info[1]}")
            elif info[0] == "health":
                st.subheader(f"Has health of {info[1]}")

    if submit:
        with st.spinner(f"Searching picks for brawler {brawler}..."):
            brawler_tags = get_map_tag(get_properties(brawler))

            res = []
            for map in get_maps():
                map = map.split(" > ")[1]
                compatibility = int(calculate_compatibility(
                    brawler_map_tags=brawler_tags,
                    map_map_tags=get_map_tag(get_properties(map)),
                ) * 100)
                added = False
                if len(res) > 0:
                    for i in range(len(res)):
                        if res[i][0] < compatibility:
                            res.insert(i, [compatibility, map])
                            added = True
                            break
                if not added:
                    res.append([compatibility, map])
            for row in res:
                st.subheader(f"{row[0]}% with map {row[1]}")


def get_map_tag(tags):
    return [info[1] for info in tags if info[0] == "hasMapTag"]


def calculate_compatibility(brawler_map_tags, map_map_tags):
    if len(map_map_tags) > 0 and len(brawler_map_tags) > 0:
        count = 0
        for tag in map_map_tags:
            if tag in brawler_map_tags:
                count += 1
        return min(1, count / len(map_map_tags))
    return 0


def compatibility_ui() -> None:
    with st.sidebar:
        compatibility_form = st.form("CompatiblityForm")
        compatibility_form.title("Map & Brawler compatibility")
        map = compatibility_form.selectbox("Map", get_maps()).split(" > ")[1]
        brawler = compatibility_form.selectbox("Brawler", get_brawlers()).split(" > ")[
            1
        ]
        submit = compatibility_form.form_submit_button(
            "See compatibility", use_container_width=True
        )

    if submit:
        with st.spinner(
            f"Calculating compatibility between map {map} and brawler {brawler} ..."
        ):
            map_properties = get_properties(map)
            brawler_properties = get_properties(brawler)

        left, middle, right = st.columns([1, 1, 1])

        map_tags = get_map_tag(map_properties)
        left.header(f"Map {map}")
        left.json(map_tags)
        # left.json(map_properties, expanded=False)

        brawler_tags = get_map_tag(brawler_properties)
        right.header(f"Brawler {brawler}")
        right.json(brawler_tags)
        # right.json(brawler_properties, expanded=False)

        middle.header(
            f"Compatibility of {int(calculate_compatibility(brawler_tags, map_tags) * 100)}%"
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Web Sementique Ales",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    # Load BDD
    with st.sidebar:
        with st.spinner("Loading RDF DataBase"):
            if not load_rdf_file():
                st.error("Error loading RDF DataBase !")
                st.stop()
        # st.success("RDF DataBase successfully loaded")

    # Display UI
    compatibility_ui()
    map_ui()
    brawler_ui()
