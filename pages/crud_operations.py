import streamlit as st
import pandas as pd
import utils.db_connection as db
import time

st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
            border-radius: 12px;
            padding: 30px;
        }

        /* Title */
        h1 {
            text-align: center;
            color: #2c3e50;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Streamlit Input and Select Fields */
        div[data-baseweb="input"]{
            border: 2px solid #b0c4de !important;
            border-radius: 8px !important;
            padding: 10px !important;
            /*background-color: white !important;
            color: #2c3e50 !important;*/
        }
        div[data-baseweb="select"] > div{
            border: 2px solid #b0c4de !important;
            border-radius: 8px !important;
        }

        /* Input Focus Effect */
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border: 2px solid #007BFF !important;
            box-shadow: 0 0 5px #007BFF !important;
            
        }
        
        div[data-baseweb="toaster"]{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            position: absolute;
            bottom: 100px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }

        /* Dataframe Table */
        .player-table th {
            background-color: #2e86de;
            color: white;
            text-align: center;
            padding: 8px;
        }
        .player-table td {
            text-align: center;
            padding: 6px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏏 Cricket Player Management System")

# --------------------- OPERATION SELECTOR ---------------------
operation = st.selectbox(
    "Choose an operation:",
    ["Create", "Read", "Update", "Delete"]
)

st.markdown("---")

# --------------------- CREATE OPERATION ---------------------
if operation == "Create":
    with st.form("create_form", clear_on_submit=True):
        st.subheader("➕ Add New Player")

        col1, col2 = st.columns(2)
        with col1:
            player_name = st.text_input("Player Name")
            playing_role = st.selectbox("Playing Role", ["BATSMEN","BOWLER","ALL ROUNDER","WICKET KEEPER"])
            batting_style = st.text_input("Batting Style")
        with col2:
            bowling_style = st.text_input("Bowling Style")
            team = st.text_input("Team")

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if(player_name != ""):
               max_record= db.fetch_records("SELECT (max(player_id)+1) as new_player_id FROM players")
               new_player_id = int(max_record['new_player_id'][0])
               sucessfull = db.execute(query="""
                INSERT INTO players (player_id, player_name, playing_role, batting_style, bowling_style, team)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, params=(new_player_id,player_name, playing_role, batting_style, bowling_style, team))
               if sucessfull:
                #st.info(f"new player id {new_player_id}")
                st.toast(f"✅ Player '{player_name}' added successfully!",)
            else:
                st.warning("Please provide player name. It's mandatory..")
# --------------------- READ OPERATION ---------------------
elif operation == "Read":
    st.subheader("📋 Search & View Player Records")

    # Search Filters
    with st.container():
        search_col1, search_col2 = st.columns([2, 1])
        with search_col1:
            search_query = st.text_input("Search by Player Name or ID", placeholder="Enter player name or ID...")
        with search_col2:
            search_button = st.button("🔍 Search")

    # Fetch data
    if search_button and search_query:
        if search_query.isdigit():
            records = pd.read_sql(f"SELECT * FROM players WHERE player_id = {search_query}", db.create_connection())
        else:
            records = pd.read_sql(f"SELECT * FROM players WHERE lower(player_name) LIKE '%{search_query.lower()}%'", db.create_connection())
    else:
        records = pd.read_sql("SELECT * FROM players", db.create_connection())

    # Display Table
    if not records.empty:
        st.markdown("### Player Records")
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
    
        styled_html = records.to_html(index=False, classes="styled-table")

        st.markdown(styled_html, unsafe_allow_html=True)
    else:
        st.info("No records found.")

# --------------------- UPDATE OPERATION ---------------------
elif operation == "Update":
    st.subheader("✏️ Update Player Details")
    players_records = pd.read_sql("SELECT * FROM players", db.create_connection())

    if not players_records.empty:
        #players_records_list = players_records.tolist()
        player_ids = players_records.iloc[:,0:2].values.tolist()
        player_ids.insert(0,["Choose Player",""])
        selected_id = st.selectbox("Select Player ID to Update",player_ids,on_change=lambda:st.session_state.update({"show_update_form": True}),key="update_player_profile")
        selected_id = selected_id[0]
        selected_player = None
        if selected_id != "Choose Player":
            selected_player = players_records[players_records["player_id"] == selected_id].iloc[0]

        if selected_player is not None and st.session_state.get("show_update_form"):
            with st.form("update_form"):
                new_name = st.text_input("Player Name", value=selected_player["player_name"])
                # role select list logic starts here
                role_list = ["BATSMEN","BOWLER","ALL ROUNDER","WICKET KEEPER"]
                role_value = selected_player["playing_role"].strip().upper()
                role_index = role_list.index(role_value)
                new_role = st.selectbox("Playing Role",role_list,index=role_index)
                # role logic end here
                new_batting = st.text_input("Batting Style", value=selected_player["batting_style"])
                new_bowling = st.text_input("Bowling Style", value=selected_player["bowling_style"])
                new_team = st.text_input("Team", value=selected_player["team"])

                update_btn = st.form_submit_button("Update Player")

                if update_btn:
                    st.session_state.show_update_form = False
                    sucessfull = db.execute("""
                        UPDATE players 
                        SET player_name=%s, playing_role=%s, batting_style=%s, bowling_style=%s, team=%s
                        WHERE player_id=%s
                    """, (new_name, new_role, new_batting, new_bowling, new_team, selected_id))
                    if sucessfull:
                        st.toast("✅ Player details updated successfully!")
                        time.sleep(1)
                        st.rerun()
                        del st.session_state["update_player_profile"]
    else:
        st.info("No players available to update.")

# --------------------- DELETE OPERATION ---------------------
elif operation == "Delete":
    st.subheader("🗑️ Delete Player Record")
    players_records_1 = pd.read_sql("SELECT * FROM players", db.create_connection())

    if not players_records_1.empty:
        #players_records_list = players_records.tolist()
        player_ids_1 = players_records_1.iloc[:,0:2].values.tolist()
        player_ids_1.insert(0,["Choose Player",""])
        selected_id = st.selectbox("Select Player ID to Update",player_ids_1,key="delete_player_profile")
        selected_id = selected_id[0] #extracting id from list which has format of [id,name]
        
        if selected_id == "Choose Player":
            selected_id = None

        if selected_id is not None:
            selected_player = players_records_1[players_records_1["player_id"] == selected_id].iloc[0]
            st.warning(f"Are you sure you want to delete **{selected_player['player_id']} -- {selected_player['player_name']} ({selected_player['team']})**?")


        if st.button("Delete Player", type="primary",on_click=lambda:st.session_state.update({"delete_player":True})) and selected_id is not None and st.session_state.get("delete_player"):
            st.session_state.delete_player = False
            sucessfull = db.execute("DELETE FROM players WHERE player_id=%s", (selected_id,))
            if sucessfull:
                st.toast("✅ Player deleted successfully!")
                time.sleep(1)
                st.rerun()
                del st.session_state["delete_player_profile"]
    else:
        st.info("No players available to delete.")
