import streamlit as st
import pandas as pd
import utils.db_connection as db
import requests


headers = {
	"x-rapidapi-key": "2ff514151fmsh912ff982e96dabbp19c56cjsnea7d12a552fa",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}


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
    "3":"SELECT * FROM most_runs ORDER BY total_runs_scored",
}


create_query_ = [

]

options = ["-- Select a question --"] + list(sql_questions.values())
st.header("SQL Analysis")
st.subheader("Questions")
selected_question   = st.selectbox("", options,width=1000)
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

    if selected_qid == "3":
        query = "create table if not exists most_runs(player_id int primary key,player_name varchar,total_runs_scored int,batting_average decimal)"
        db.execute(query=query)
        try:
            url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

            querystring = {"statsType":"mostRuns","matchType":"2"}

            response = requests.get(url, headers=headers, params=querystring)
            response_most_runs = response.json()

            for most_runs in response_most_runs.get('values',{}):
                player_id   = most_runs['values'][0]
                player_name = most_runs['values'][1]
                runs        = most_runs['values'][4]
                average     = most_runs['values'][5]
                most_runs_list = {"player_id":player_id,"player_name":player_name,"total_runs_scored":runs,"average":average}
                query = "insert into most_runs (player_id,player_name,total_runs_scored,batting_average) values (%s,%s,%s,%s)"
                db.execute(query=query,params=most_runs_list)

        except Exception as e:
            print("Error Occured",e)

