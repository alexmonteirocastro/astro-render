import streamlit as st

from astro_engine import (
    HouseSystem,
    aspects_table,
    get_chart,
    get_IANA_tz,
    get_place_coordinates,
    houses_table,
    planets_table,
    render_astrological_chart,
)

st.set_page_config(page_title="Astro Engine", layout="centered")
st.title("Astro Data Calculator")

place = st.text_input("Place", "Gdynia, Poland")
date = st.text_input("Date (YYYY-MM-DD)", "2025-12-28")
time = st.text_input("Time (HH:MM)", "12:30")

HOUSE_LABELS = {
    HouseSystem.PLACIDUS: "Placidus",
    (
        HouseSystem.REGIOMONTANANUS
        if hasattr(HouseSystem, "REGIOMONTANANUS")
        else HouseSystem.REGIOMONTANUS
    ): "Regiomontanus",
    HouseSystem.EQUAL_HOUSES: "Equal Houses",
    HouseSystem.WHOLE_SIGN: "Whole Sign",
    HouseSystem.TOPOCENTRIC: "Topocentric",
    HouseSystem.MORINUS: "Morinus",
}

house_system = st.selectbox(
    "House system",
    options=list(HOUSE_LABELS.keys()),
    format_func=lambda hs: HOUSE_LABELS[hs],
    index=list(HOUSE_LABELS.keys()).index(HouseSystem.PLACIDUS),
)

run = st.button("Calculate chart")

if run:
    try:
        coords = get_place_coordinates(place)
        tz_id = get_IANA_tz(latitude=coords.latitude, longitude=coords.longitude)

        data = get_chart(
            date=date,
            time=time,
            latitude=coords.latitude,
            longitude=coords.longitude,
            house_system=house_system,
            timezone_IANA_id=tz_id,
        )

        st.success(f"Timezone: {tz_id}")

        st.subheader("Chart")
        fig = render_astrological_chart(data)
        st.pyplot(fig, clear_figure=True, width="content")

        # tables
        st.subheader("Planets")
        st.dataframe(planets_table(data), width="content")  # type: ignore

        st.subheader("House cusps")
        st.dataframe(houses_table(data), width="content")  # type: ignore

        st.subheader("Aspects")
        st.dataframe(aspects_table(data), width="content")  # type: ignore

        with st.expander("View Raw Data"):
            st.json(data.model_dump(), expanded=False)

    except Exception as e:
        st.error(str(e))
