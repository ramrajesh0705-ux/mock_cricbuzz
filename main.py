import streamlit as st

st.set_page_config(page_title="🏏 Cricbuzz App", page_icon="🏏", layout="wide")

pg = st.navigation(
    [   st.Page("pages/home.py",title="Home"),
        st.Page("pages/live_matches.py",title="Live Matches"),
        st.Page("pages/player_stats.py",title="Player Stats"),
        st.Page("pages/sql_queries.py",title = "Sql Analysis"),
        st.Page("pages/crud_operations.py",title="Crud Operations")
    ]
    )

pg.run()