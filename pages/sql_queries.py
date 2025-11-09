import streamlit as st
import pandas as pd
import utils.db_connection as db
import requests
from datetime import datetime


headers = {
	"x-rapidapi-key": "2ff514151fmsh912ff982e96dabbp19c56cjsnea7d12a552fa",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

st.markdown("""
            <style>
            div[data-baseweb="select"] > div{
                border: 2px solid #b0c4de !important;
                border-radius: 8px !important;
            }
            </style>

            """,unsafe_allow_html=True)
sql_questions = {
     "1": " 1. Find all players who represent India. Display their full name, playing role, batting style, and bowling style."
    ,"2": " 2. Show all cricket matches that were played in the last Few days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first."
    ,"3": " 3. List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first."
    ,"4": " 4. Display all cricket venues that have a seating capacity of more than 30,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first."
    ,"5": " 5. Calculate how many matches each team has won. Show team name and total number of wins. Display teams with the most wins first."
    ,"6": " 6. Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role."
    ,"7": " 7. Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format."
    ,"8": " 8. Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned."
}

query_table = {
    "1":"SELECT  player_name,playing_role,batting_style,bowling_style FROM players",
    "2":"SELECT  match_description,team_1_name as team1,team_2_name as team2,venue_name,match_date FROM recent_matches ORDER BY match_date DESC",
    "3":"SELECT  player_name,runs as total_runs_scored,average as batting_average FROM most_runs_stats WHERE format = 'ODI' ORDER BY total_runs_scored DESC",
    "4":"select ground as venue_name,city,country,capacity as seating_capacity from venue_info where capacity::NUMERIC > 30000 order by capacity::NUMERIC desc;",
    "5":"",
    "6":"SELECT playing_role,count(*) from players group by playing_role",
    "7":"SELECT format as match_format,max(highest_score) as highest_score from highest_score_stats group by format",
}


create_query_ = [

]

options = ["-- Select a question --"] + list(sql_questions.values())
st.header("SQL Analysis")
st.subheader("Questions")
selected_question   = st.selectbox("Choose a question", options,width=1000)
selected_qid        = None
for k, v in sql_questions.items():
    if v == selected_question:
        selected_qid = k
        break

if selected_qid is not None:
    st.markdown(f"### 🧠 Question {selected_qid}:")
    st.info(sql_questions[selected_qid])

    st.subheader("Query:")
    st.code(f"{query_table.get(selected_qid)}",language="sql")
    fetch_query = query_table.get(selected_qid,'')
    result = db.fetch_records(fetch_query)
        
    st.markdown("""
            <style>
            .styled-table {
                width: 1000px;
                border-collapse: collapse;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                text-align: center;
                background-color: #f8fafc;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .styled-table th {
                background-color: #2563eb;
                color: white;
                padding: 10px;
                font-weight: bold;
                text-align:center;
            }
            .styled-table td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            .styled-table tr:nth-child(even) {
                background-color: #f1f5f9;
            }
            .styled-table tr:hover {
                background-color: #dbeafe;
            }
            </style>
            """, unsafe_allow_html=True)
    
    styled_html = result.to_html(index=False, classes="styled-table")

    st.markdown(styled_html, unsafe_allow_html=True)
