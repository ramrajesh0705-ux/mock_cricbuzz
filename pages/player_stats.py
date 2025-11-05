import streamlit as st
import requests
import pandas as pd

#search_player_url =


player_search_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
headers = {
	"x-rapidapi-key": "2ff514151fmsh912ff982e96dabbp19c56cjsnea7d12a552fa",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}


def fetch_player_list(player_name):
    querystring = {"plrN":player_name}
    try:
        response = requests.get(player_search_url, headers=headers,params=querystring)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print("Exception occurred:", e)
        return {}




# --- Title & Search Layout ---
st.title("🏏 Cricket Player Statistics")
st.subheader("🔍 Search For Player Here")
st.divider()
searched_player_name = st.text_input(
        "Type player name",
        placeholder="Enter the player name here",
        key="searched_player_name",
        width=1000
    )
search_button = st.button("Search", type="primary")    

st.divider()

# --- SEARCH BUTTON CLICK LOGIC---
if search_button:
    if searched_player_name:
        players_response = fetch_player_list(searched_player_name)
        players = players_response.get('player', [])
        st.session_state["players"] = players  # store players in session
        st.session_state["searched"] = True

# --- AFTER SEARCH ---
if st.session_state.get("searched"):
    players = st.session_state.get("players", [])
    if len(players) == 1:
        st.session_state['player_id'] = players[0]['id']
    elif len(players) > 1:
        player_list_options = {
            f"{p['name']} ({p['teamName']})": p['id'] for p in players
        }

        # Selectbox value stored in session
        selected_player = st.selectbox(f"Search results for {searched_player_name}",
                                        ["----Select ----"] + list(player_list_options.keys()),
                                        key="selected_player",
                                        on_change=lambda: st.session_state.update({"player_id": player_list_options.get(st.session_state.selected_player)}),
                                        width=1000
                                      )



if 'player_id' in st.session_state:
    player_info_url   = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state['player_id']}"
    batting_stats_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state['player_id']}/batting"
    bowling_stats_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state['player_id']}/bowling"

#get_player_info

def get_player_info():
    print("Player info url:"+player_info_url)
    try:
        response = requests.get(player_info_url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        print("Exception occurred:", e)
        return {}

#Batting stats


def get_batting_stats():
    print("batting_stats_url:"+batting_stats_url)
    try:
        response = requests.get(batting_stats_url, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print("Exception occurred:", e)
        return {}


#Bowling_stats

def get_bowling_stats():
    print("get_bowling_stats:"+bowling_stats_url)
    try:
        response = requests.get(bowling_stats_url, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print("Exception occurred:", e)
        return {}



#---- AFTER SELECTED A PLAYER
if 'player_id' in st.session_state:
    if st.session_state.get('player_id'):
        player_info = get_player_info()
        st.header(f"{player_info['name']} - Player Profile")
        image_column,names_coulmn = st.columns([1,2])
        with image_column:
            st.image({player_info['image']},width=30)
        with names_coulmn:
            st.markdown(f""" **Name  :** {player_info['name']}""")
            st.markdown(f""" **Nick Name :** {player_info['nickName']}""")

        profile_tab,batting_tab,bowling_tab = st.tabs(['Profile','Batting Stats','Bowling Stats'])

        with profile_tab:
            st.markdown("### Personal Information")
            personal_info = {
                    "Country" : player_info.get("intlTeam",'-'),
                    "Born": player_info.get("DoB",'-'),
                    "Birth Place": player_info.get("birthPlace",'-'),
                    "Role": player_info["role"],
                    "Batting Style": player_info.get("bat",'-'),
                    "Bowling Style": player_info.get("bowl",'-')
                }

            # Create an HTML table for personal info
            personal_table = "<table style='width:100%; border-collapse:collapse;'>"
            for key, value in personal_info.items():
                    personal_table += (
                        f"<tr><td style='font-weight:bold; width:30%; padding:5px;'>{key}</td>"
                        f"<td style='padding:5px;'>{value}</td></tr>"
                    )
            personal_table += "</table>"
            st.markdown(personal_table, unsafe_allow_html=True)

            # --- ICC Rankings Section ---
            st.markdown("### ICC Rankings")

            rank_tabs = st.tabs(["Batting", "Bowling", "All-Rounder"])
            rankings_info = player_info.get('rankings',{})
            with rank_tabs[0]:
                bat = rankings_info.get('bat',{})
                bat_ranks = {
                    'FORMAT': ['TEST','ODI','T20'],
                    'CURRENT RANK' : [bat.get('testRank','-'),bat.get('odiRank','-'),bat.get('t20iRank','-')],
                    'BEST RANK'    : [bat.get('testBestRank','-'),bat.get('odiBestRank','-'),bat.get('testBestRank','-')]
                }
                bat_df = pd.DataFrame(bat_ranks);
                st.table(bat_df)
            with rank_tabs[1]:
                bowl = rankings_info.get('bowl',{})
                bowl_ranks = {
                    'FORMAT': ['TEST','ODI','T20'],
                    'CURRENT RANK' : [bowl.get('testRank','-'),bowl.get('odiRank','-'),bowl.get('t20iRank','-')],
                    'BEST RANK'    : [bowl.get('testBestRank','-'),bowl.get('odiBestRank','-'),bowl.get('testBestRank','-')]
                }
                bowl_df = pd.DataFrame(bowl_ranks)
                st.table(bowl_df)
            with rank_tabs[2]:
                all_rounder = rankings_info.get('all_rounder',{})
                all_rounder_ranks = {
                    'FORMAT': ['TEST','ODI','T20'],
                    'CURRENT RANK' : [all_rounder.get('testRank','-'),all_rounder.get('odiRank','-'),all_rounder.get('t20iRank','-')],
                    'BEST RANK'    : [all_rounder.get('testBestRank','-'),all_rounder.get('odiBestRank','-'),all_rounder.get('testBestRank','-')]
                }
                all_rounder_df = pd.DataFrame(all_rounder_ranks)
                st.table(all_rounder_df)
            ##BIO
            with st.container():
                st.markdown("### Bio")
                st.markdown(player_info.get('bio',''),unsafe_allow_html=True)

            ##More info
            st.link_button(label="More info - Visit",url=player_info['appIndex'].get('webURL'))
        with batting_tab:
            st.markdown("### Batting Career")
            player_batting_stats = get_batting_stats()
            batting_career_table    = "<table>"
            bat_status_heading      = f"""<tr><th></th>
                                            <th>{player_batting_stats.get('headers')[1]}</th>
                                            <th>{player_batting_stats.get('headers')[2]}</th>
                                            <th>{player_batting_stats.get('headers')[3]}</th>
                                            <th>{player_batting_stats.get('headers')[4]}</th>
                                          </tr>
                                        """
            batting_stas_rows       = ""
            for batting_stat_values in player_batting_stats.get('values',{}):
                batting_stat_rows   = "<tr>"
                table_data          = ""
                for index,value in enumerate(batting_stat_values.get('values',[]),start=0):
                    #print(value)
                    if index == 0:
                        table_data += f"""<th>{value}</th>"""
                    else:
                        table_data += f"""<td>{value}"""
                batting_stas_rows   += table_data +  "</tr>"

            batting_career_table += bat_status_heading + batting_stas_rows + "</table>"
            st.markdown(batting_career_table, unsafe_allow_html=True)
        with bowling_tab:
            st.markdown("### Bowling Career")
            player_bowling_stats = get_bowling_stats()
            bowling_career_table    = "<table>"
            bowling_status_heading      = f"""<tr><th></th>
                                            <th>{player_bowling_stats.get('headers')[1]}</th>
                                            <th>{player_bowling_stats.get('headers')[2]}</th>
                                            <th>{player_bowling_stats.get('headers')[3]}</th>
                                            <th>{player_bowling_stats.get('headers')[4]}</th>
                                          </tr>
                                        """
            bowling_stas_rows       = ""
            for bowling_stat_values in player_bowling_stats.get('values',{}):
                bowling_stat_rows   = "<tr>"
                table_data          = ""
                for index,value in enumerate(bowling_stat_values.get('values',[]),start=0):
                    #print(value)
                    if index == 0:
                        table_data += f"""<th>{value}</th>"""
                    else:
                        table_data += f"""<td>{value}"""
                bowling_stas_rows   += table_data +  "</tr>"

            bowling_career_table += bowling_status_heading + bowling_stas_rows + "</table>"
            st.markdown(bowling_career_table, unsafe_allow_html=True)

                                                                                
