import requests
import streamlit as st
import pandas as pd

live_matches_list_url   = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
recent_matches_list_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
	"x-rapidapi-key": "096090eac4mshd73dfcde8a35834p1911efjsn4dcdb491bdcc",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}


def get_matches_list(data):
    
    
    matches_list    = []
    typeMatches     = data.get('typeMatches',[])
    for typeMatch in typeMatches:
        series_matches = typeMatch.get('seriesMatches',[])
        for series in series_matches:
            series_data = series.get('seriesAdWrapper',{})
            series_id   = series_data.get('seriesId')
            series_name = series_data.get('seriesName')
            matches     = series_data.get('matches',[])
            for match in matches:
                match_info      = match.get('matchInfo',{})
                match_id        = match_info.get('matchId','')
                match_desc      = match_info.get('matchDesc','')
                match_format    = match_info.get('matchFormat','')
                start_date      = match_info.get('startDate','')
                team1           = match_info.get('team1',{})
                team1_name      = team1.get('teamName')
                team2           = match_info.get('team2',{})
                team2_name      = team2.get('teamName','')
                state           = match_info.get('state','')
                venue_info      = match_info.get('venueInfo',{})
                venue           = venue_info.get("ground",'')
                city            = venue_info.get('city','')
                venue_detail    = venue+","+city
                team1_scr_desc  = ""
                team2_scr_desc  = ""
                status          = match_info.get('status','')

                match_scores    = match.get('matchScore',{})
                team1_score     = match_scores.get('team1Score',{})
            
                for count,innings in enumerate(team1_score.keys(),start = 0):
                    runs            = team1_score[innings].get('runs','')
                    wickets         =str(team1_score[innings].get('wickets',''))
                    if(wickets == "None" or wickets == ''):
                        wickets = "0"
                    overs           = team1_score[innings].get('overs','')
                    if(count > 0):
                        team1_scr_desc += ' & '
                    team1_scr_desc  = team1_scr_desc+""+str(runs)+"-"+wickets+" ("+str(overs)+")"
                team2_score     = match_scores.get('team2Score',{})
                for count,innings in enumerate(team2_score.keys(),start = 0):
                    runs            = team2_score[innings].get('runs')
                    wickets         = str(team2_score[innings].get('wickets'))
                    if(wickets == "None" or wickets == ''):
                        wickets = "0"
                    overs           = team2_score[innings].get('overs')
                    if(count > 0):
                        team2_scr_desc += ' & '
                    team2_scr_desc  = team2_scr_desc+""+str(runs)+"-"+wickets+" ("+str(overs)+")"
                    
                #print(team1_scr_desc,"        ",team2_scr_desc)
                matches_list.append({
                    "series_id":series_id
                    ,"series_name" : series_name
                    ,"match_id":match_id
                    ,"match_desc":match_desc
                    ,"match_format":match_format
                    ,"start_date":start_date
                    ,"team1_name":team1_name
                    ,"team2_name":team2_name
                    ,"state":state
                    ,"venue_detail":venue_detail
                    ,"team1_score_desc":team1_scr_desc
                    ,"team2_score_desc":team2_scr_desc
                    ,"status":status
                })
    return matches_list

@st.cache_data(ttl=300) # cache for 5 minutes d
def fetch_matches_list():
    try:
        response = requests.get(live_matches_list_url, headers=headers)
        response.raise_for_status()
        live_matches_data = response.json()
    
        if isinstance(live_matches_data, dict) and "typeMatches" in live_matches_data and live_matches_data["typeMatches"]:
            #print("The data receive successfully",live_matches_data)
            return get_matches_list(live_matches_data)
        else:
            recent_match_response = requests.get(recent_matches_list_url, headers=headers)
            recent_match_response.raise_for_status()
            recent_matches_data = recent_match_response.json()
            return get_matches_list(recent_matches_data)

    except Exception as e:
        print("Exception occurred:", e)
        return {}


matches_list = fetch_matches_list()


def prepare_matches_list_options(matches_list_dict):
     return {f"{match['team1_name']} vs {match['team2_name']}- {match['match_desc']} ({match['state']})":match['match_id'] for match in matches_list_dict} # dictionary comprehension


## Live Matches Page
st.title("🏏 Live Cricket Score Dashboard")

if not matches_list:
    st.warning("No matches found right now.")
    st.stop()

# Prepare select options
matches_options =  prepare_matches_list_options(matches_list)

# Maintain session-safe selection
st.subheader("Select a match to view details")
selected_match = st.selectbox(
    "Available Matches",
    ["-- Select a Match --"] + list(matches_options.keys()),
    key="match_select",
    width=1000
)

selected_match_detail = None
match_id              = None
# Defensive check before accessing dictionary
if selected_match and selected_match != "-- Select a Match --" and selected_match in matches_options:
    match_id = matches_options[selected_match]
    selected_match_detail = next(
        (m for m in matches_list if m["match_id"] == match_id),
        {}
    )
if selected_match_detail is not None:
    st.markdown(f"## ⚔️ {selected_match_detail.get('team1_name')} vs {selected_match_detail.get('team2_name')}")
    match_detail,series_detail = st.columns(2)
    with match_detail:
        st.markdown(f"""📅**Match  :** {selected_match_detail.get('match_desc')}""" )
        st.markdown(f"""🏆**Format :** {selected_match_detail.get('match_format')}""")
        st.markdown(f"""🏟️**Venue  :** {selected_match_detail.get('venue_detail')}""")
        st.markdown(f"""📈**Status :** {selected_match_detail.get('status')}""")
        st.markdown(f"""🛡️**State  :** {selected_match_detail.get('state')}""")

    with series_detail:
        st.markdown(f"""🏅**Series :** {selected_match_detail.get('series_name')}""")

    st.markdown("## Current Score")
    team1_score_desc,team2_score_desc = st.columns(2)
    with team1_score_desc:
        st.markdown(f"**{selected_match_detail.get('team1_name')}**")
        st.text(selected_match_detail.get('team1_score_desc'))
    with team2_score_desc:
        st.markdown(f"**{selected_match_detail.get('team2_name')}**")
        st.text(selected_match_detail.get('team2_score_desc'))

    ### Logic To Fetch Live Match Score Card Based on the Selected Match Id

    match_score_card_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

    def fetch_match_scorecard():
        try:
            response = requests.get(match_score_card_url, headers=headers)
            response.raise_for_status()
            match_score_card_data = response.json()
            return match_score_card_data
        except Exception as e:
            print("Exception occurred:", e)
            return {}

    view_score_card = st.button("View Score Card")
 
    if view_score_card:
        scored_card_row_detail = ""
        match_score_card = fetch_match_scorecard()
        
        print("called ",match_id)
        scored_card = match_score_card.get('scorecard',[])
        for innings_score_card in scored_card:
            innings_header_row = f"""<tr><th colspan='7' class='section-header'>Innings : {innings_score_card.get('inningsid')}</th></tr>"""

            ## Batting Team Status

            team_name_row             = team_name_row = f"""<tr><th colspan='7' class='section-header'>{innings_score_card.get('batteamname')}</th></tr>"""

            batsman_data              = innings_score_card.get('batsman',[])
            
            batsman_data_row = f"""
                            <tr style='background-color:#0066cc;color:white;font-weight:bold;'>
                            <td>Batsman</td>
                            <td>Out Desc</td>
                            <td>Runs</td>
                            <td>Balls</td>
                            <td>Fours</td>
                            <td>Sixes</td>
                            <td>Strike Rate</td>
                            </tr>
                            """
            
            for batsman in batsman_data:
                batsman_data_row += f"""<tr 'style = width:100%'><td 'style = width:20%;'>{batsman.get('name')}{' (C)' if batsman.get('iscaptain') else ''}{' (WK)' if batsman.get('iskeeper') else ''}</td><td 'style = width:40%;'>{batsman.get('outdec')}</td><td>{batsman.get('runs')}</td><td>{batsman.get('balls')}</td><td>{batsman.get('fours')}</td><td>{batsman.get('sixes')}</td><td>{batsman.get('strkrate')}</td></tr>"""
                
            ## Extras Details 
            extras_details            = innings_score_card.get('extras')
            extras_details_row        = f"""<tr 'style = width:100%'><td>Extras</td><td>{extras_details.get('total')} (Byes-{extras_details.get('byes')},leg Byes-{extras_details.get('legbyes')},Wides-{extras_details.get('wides')},No balls-{extras_details.get('noballs')}),Penalty-{extras_details.get('penalty')}</td></tr>"""
            ## Score Details
            ##score_details             = innings_score_card.get('score',{})
            score_details_row         = f"""<tr 'style = width:100%'><td 'style= col-span:3;font-weight:bold;'>Total</td><td>{innings_score_card.get('score')} - {innings_score_card.get('wickets')} ({innings_score_card.get('overs')} Overs , RR : {innings_score_card.get('runrate')}) </td></tr>"""

            ## Bowling Team Status

            bowler_data               = innings_score_card.get('bowler',[])
            bowler_data_row = f"""
                <tr style='background-color:#0066cc; color:white; font-weight:bold; text-align:center;'>
                <td>Bowler</td>
                <td>Overs</td>
                <td>Maidens</td>
                <td>Runs</td>
                <td>Wickets</td>
                <td>Economy</td>
                </tr>
                """
            for bowler in bowler_data:
                bowler_data_row += f"""<tr><td>{bowler.get('name')}</td><td>{bowler.get('overs')}</td><td>{bowler.get('maidens')}</td><td>{bowler.get('runs')}</td><td>{bowler.get('wickets')}</td><td>{bowler.get('economy')}</td></tr>"""

            ## Fall of Wickets
            fall_of_wickets__details  = innings_score_card.get('fow',{}).get('fow',[])
            fall_of_wkts_data_row     = f"""<tr style='background-color:#0066cc; color:white; font-weight:bold; text-align:center;'><td>Fall Of Wickets</td><td>Score</td><td>Overs</td></tr>"""

            for count,wicket_data in enumerate(fall_of_wickets__details,start=1):
                fall_of_wkts_data_row     += f"""<tr 'style = width:100%'><td 'style = width:20%;'>{wicket_data.get('batsmanname')}</td><td>{wicket_data.get('runs')} - {count}</td><td>{wicket_data.get('overnbr')}</td></tr>"""

            ## Power Play
            power_play_details        = innings_score_card.get('pp',{}).get('powerplay',[])
            power_play_details_row    = f"""<tr 'style = width:100%'><th 'style = width:20%;'>Power Plays</th><th>Score</th><th>Overs</th></tr>"""
            for power_play in power_play_details:
                power_play_details_row += f"""<tr 'style = width:100%'><td 'style = width:20%;'>{power_play.get('pptype')}</td><td>{power_play.get('ovrfrom')} - {power_play.get('ovrto')}</td><td>{power_play.get('run')}-{power_play.get('wickets')}</td></tr>"""

            ## Partnership Details
            partnership_details       = innings_score_card.get('partnership',{}).get('partnership')
            partnerships_details_row    = f"""<tr 'style = width:100%'><th colspan=3>Partnerships</th></tr>"""

            for partnership in partnership_details:
                partnerships_details_row += f"""<tr><td>{partnership.get('bat1name')}-{partnership.get('bat1runs')}({partnership.get('bat1balls')})</td><td>{partnership.get('totalruns')}({partnership.get('totalballs')})</td><td>{partnership.get('bat2name')}-{partnership.get('bat2runs')}({partnership.get('bat2balls')})</td></tr>"""

            scored_card_row_detail += innings_header_row + team_name_row + batsman_data_row + extras_details_row +  score_details_row + bowler_data_row + fall_of_wkts_data_row + power_play_details_row + partnerships_details_row



        html_table = f"""
                <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-family: 'Segoe UI', sans-serif;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    text-align: center;
                    padding: 8px;
                }}
                th {{
                    background-color: #0066cc;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f6fc;
                }}
                tr:nth-child(odd) {{
                    background-color: #ffffff;
                }}
                td {{
                    font-size: 13px;
                }}
                .section-header {{
                    background-color: #004080;
                    color: #ffffff;
                    font-weight: bold;
                    text-align: center;
                    font-size: 15px;
                    padding: 6px;
                }}
            </style>
            <table style='width:100%; border-collapse: collapse;'>
            {scored_card_row_detail}
            </table>
            """
        st.markdown(html_table, unsafe_allow_html=True)

            