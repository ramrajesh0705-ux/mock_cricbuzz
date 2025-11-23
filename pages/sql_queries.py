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
     "1" : " 1. Find all players who represent India. Display their full name, playing role, batting style, and bowling style."
    ,"2" : " 2. Show all cricket matches that were played in the last Few days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first."
    ,"3" : " 3. List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first."
    ,"4" : " 4. Display all cricket venues that have a seating capacity of more than 30,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first."
    ,"5" : " 5. Calculate how many matches each team has won. Show team name and total number of wins. Display teams with the most wins first."
    ,"6" : " 6. Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role."
    ,"7" : " 7. Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format."
    ,"8" : " 8. Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned."
    ,"9" : " 9. Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name, total runs, total wickets, and the cricket format."
    ,"10": "10. Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first."
    ,"11": "11. Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test cricket, ODI cricket, and T20I cricket, along with their overall batting average across all formats."
    ,"12": "12. Analyze each international team's performance when playing at home versus playing away. Determine whether each team played at home or away based on whether the venue country matches the team's country. Count wins for each team in both home and away conditions."
    ,"13": "13. Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings. Show both player names, their combined partnership runs, and which innings it occurred in."
    ,"14": "14. Examine bowling performance at different venues. For bowlers who have played at least 3 matches at the same venue, calculate their average economy rate, total wickets taken, and number of matches played at each venue. Focus on bowlers who bowled at least 4 overs in each match"
    ,"15": "15. Identify players who perform exceptionally well in close matches. A close match is defined as one decided by less than 50 runs OR less than 5 wickets. For these close matches, calculate each player's average runs scored, total close matches played, and how many of those close matches their team won when they batted."
    ,"16": "16. Track how players' batting performance changes over different years. For matches since 2020, show each player's average runs per match and average strike rate for each year. Only include players who played at least 5 matches in that year."
    ,"17": "17. Investigate whether winning the toss gives teams an advantage in winning matches. Calculate what percentage of matches are won by the team that wins the toss, broken down by their toss decision (choosing to bat first or bowl first)."
    ,"18": "18. Find the most economical bowlers in limited-overs cricket (ODI and T20 formats). Calculate each bowler's overall economy rate and total wickets taken. Only consider bowlers who have bowled in at least 10 matches and bowled at least 2 overs per match on average."
    ,"19": "19. Determine which batsmen are most consistent in their scoring. Calculate the average runs scored and the standard deviation of runs for each player. Only include players who have faced at least 10 balls per innings and played since 2022. A lower standard deviation indicates more consistent performance."
    ,"20": "20. Analyze how many matches each player has played in different cricket formats and their batting average in each format. Show the count of Test matches, ODI matches, and T20 matches for each player, along with their respective batting averages. Only include players who have played at least 20 total matches across all formats."
    ,"21": """21. Create a comprehensive performance ranking system for players. Combine their batting performance (runs scored, batting average, strike rate),
              bowling performance (wickets taken, bowling average, economy rate), and fielding performance (catches, stumpings) into a single weighted score. Use this formula and rank players:
            ●Batting points: (runs_scored × 0.01) + (batting_average × 0.5) + (strike_rate × 0.3)
            ●Bowling points: (wickets_taken × 2) + (50 - bowling_average) × 0.5) + ((6 - economy_rate) × 2)
            Rank the top performers in each cricket format.
           """
    ,"22":"""22. Build a head-to-head match prediction analysis between teams. For each pair of teams that have played at least 5 matches against each other in the last 3 years,
                 calculate:
                ●Total matches played between them
                ●Wins for each team
                ●Average victory margin when each team wins
                ●Performance when batting first vs bowling first at different venues
                ●Overall win percentage for each team in this head-to-head record
          """
    ,"23":"""23. Analyze recent player form and momentum. For each player's last 10 batting performances, calculate:
                ●Average runs in their last 5 matches vs their last 10 matches
                ●Recent strike rate trends
                ●Number of scores above 50 in recent matches
                ●A consistency score based on standard deviation
                Based on these metrics, categorize players as being in "Excellent Form", "Good Form", "Average Form", or "Poor Form".
          """
    ,"24":"""24. Study successful batting partnerships to identify the best player combinations. For pairs of players who have batted together as 
                consecutive batsmen (positions differ by 1) in at least 5 partnerships:
                ●Calculate their average partnership runs
                ●Count how many of their partnerships exceeded 50 runs
                ●Find their highest partnership score
                ●Calculate their success rate (percentage of good partnerships)
                Rank the most successful batting partnerships.
          """
    ,"25":"""25. Perform a time-series analysis of player performance evolution. Track how each player's batting performance changes over time by:
                    ●Calculating quarterly averages for runs and strike rate
                    ●Comparing each quarter's performance to the previous quarter
                    ●Identifying whether performance is improving, declining, or stable
                    ●Determining overall career trajectory over the last few years
                    ●Categorizing players' career phase as "Career Ascending", "Career Declining", or "Career Stable"
                    Only analyze players with data spanning at least 6 quarters and a minimum of 3 matches per quarter.
          """
}

query_table = {
                "1":"SELECT  player_name,playing_role,batting_style,bowling_style FROM players where team ='INDIA'",
                "2":"""SELECT  match_description,team_1_name as team1,team_2_name as team2,venue_name,match_date FROM matches 
                WHERE match_date::date > (now() - interval '15 Days')::date
                ORDER BY match_date DESC;""" ,
                "3":"""
                SELECT 
                    ms.player_id,ms.player_name,ms.runs,ms.average,coalesce(bs.hundred,0) as centuries
                FROM 
                    most_runs_stats ms
                LEFT OUTER JOIN 
                    player_career_batting_stats bs
                ON 
                    ms.player_id = bs.player_id
                    AND ms.format    = bs.format
                WHERE 
                    ms.format = 'ODI'
                ORDER BY 
                    ms.runs DESC
                LIMIT 10;
                """,
                "4":"""SELECT  ground as venue_name,city,country,capacity as seating_capacity from venue_info
                WHERE capacity::NUMERIC > 30000 
                ORDER BY capacity::NUMERIC desc;""",
                "5":""" SELECT
                        (SELECT team_name from team where team_id = x1.winning_team_id) as team_name
                        ,x1.no_of_wins as no_of_wins
                    FROM
                    (
                        SELECT 
                            winning_team_id
                            ,count(*) as no_of_wins
                        FROM
                        (
                            SELECT
                                m.*
                                ,mh.*
                            FROM 
                                matches m
                                ,match_headers mh
                                ,team t
                            WHERE
                                m.match_id = mh.match_id
                                AND mh.winning_team_id = t.team_id
                        )x
                        group by
                        x.winning_team_id
                    )x1
                    ORDER BY no_of_wins DESC
                    """,
                "6":"SELECT playing_role,count(*) from players group by playing_role",
                "7":"""SELECT format as match_format,max(highest_score) as highest_score from highest_score_stats
                GROUP BY format""",
                "8":"""
                SELECT
                    series_name,
                    host_country,
                    match_type,
                    start_date,
                    total_no_matches_planned as no_of_matches_planned
                FROM
                    series
                WHERE
                    (to_char(start_date,'yyyy'))::NUMERIC = 2024
                """,
                "9":"""
                    SELECT
                        *
                    FROM
                        (
                            SELECT
                                player_name
                                ,sum(runs) as total_runs
                                ,sum(wickets) as total_wickets
                            FROM
                            (
                                SELECT 
                                    p.player_name,
                                    b.format,
                                    b.runs as runs,
                                    bw.wickets AS wickets
                                FROM players p
                                JOIN player_career_batting_stats b 
                                    ON p.player_id = b.player_id
                                JOIN player_career_bowling_stats bw
                                    ON p.player_id = bw.player_id
                                    AND b.format = bw.format
                            )ms
                            GROUP BY
                                player_name
                        )fms
                        WHERE
                            fms.total_runs >= 1000
                            AND fms.total_wickets >= 50
                        ORDER BY
                            fms.total_runs desc,total_wickets;
                """,
                "10":"""
                    SELECT
                        m.match_description
                        ,m.team_1_name
                        ,m.team_2_name
                        ,(SELECT team_name from team where team_id = mh.winning_team_id) as winning_team_name
                        ,mh.victory_margin
                        ,mh.victory_type
                        ,m.venue_name
                    FROM
                        matches m
                    JOIN 
                        match_headers mh
                    ON
                        m.match_id = mh.match_id
                    WHERE
                        m.match_state = 'Complete'
                        AND (SELECT team_name from team where team_id = mh.winning_team_id) is not null
                    ORDER BY
                        m.match_date DESC
                    LIMIT 20
                """,
                "11":"""
                        WITH player_format_runs AS (
                            SELECT
                                b.batsman_id,
                                m.match_format,
                                SUM(b.runs) AS total_runs
                            FROM batsmen b
                            JOIN matches m ON b.match_id = m.match_id
                            WHERE match_format is not null
                            GROUP BY b.batsman_id,m.match_format
                            ORDER BY b.batsman_id
                        ),

                        player_format_count AS (
                            SELECT
                                batsman_id,
                                COUNT(DISTINCT match_format) AS formats_played
                            FROM player_format_runs
                            GROUP BY batsman_id
                        ),
                        
                        player_overall_stats AS (
                            SELECT
                                b.batsman_id,
                                SUM(b.runs) AS overall_runs,
                                COUNT(*) AS innings_played
                            FROM batsmen b
                            GROUP BY b.batsman_id
                        )
                        SELECT
                            p.player_id,
                            p.player_name,
                            COALESCE(MAX(CASE WHEN m.match_format = 'TEST' THEN m.total_runs END), 0) AS test_runs,
                            COALESCE(MAX(CASE WHEN m.match_format = 'ODI' THEN m.total_runs END), 0) AS odi_runs,
                            COALESCE(MAX(CASE WHEN m.match_format = 'T20' THEN m.total_runs END), 0) AS t20i_runs,
                            ROUND(os.overall_runs::numeric / NULLIF(os.innings_played, 0), 2) AS overall_batting_avg
                        FROM player_format_runs m
                        JOIN player_format_count f ON m.batsman_id = f.batsman_id AND f.formats_played >= 2
                        JOIN players p ON p.player_id = m.batsman_id
                        JOIN player_overall_stats os ON os.batsman_id = p.player_id
                        WHERE
                            ROUND(os.overall_runs::numeric / NULLIF(os.innings_played, 0), 2) > 0.0
                        GROUP BY
                            p.player_id,
                            p.player_name,
                            os.overall_runs,
                            os.innings_played
                        ORDER BY
                            p.player_name;
                    """,
                "12":"""
                    SELECT
                        team_name,
                        match_location,
                        COUNT(*) FILTER (WHERE win_flag = 1) AS wins
                    FROM 
                        (
                            SELECT
                            team_id,
                            team_name,
                            match_location,
                            CASE WHEN team_id = winning_team_id THEN 1 ELSE 0 END AS win_flag
                        FROM
                        (
                            SELECT
                            match_id,
                            team_id,
                            team_name,
                            team_country,
                            venue_country,
                            winning_team_id,
                            CASE 
                                WHEN team_country = venue_country THEN 'HOME'
                                ELSE 'AWAY'
                            END AS match_location
                        FROM 
                        (
                        SELECT
                            m.match_id,
                            m.team_1_name,
                            m.team_2_name,
                            v.country AS venue_country,
                            mh.winning_team_id,
                            t.team_id,
                            t.team_name,
                            t.country AS team_country
                        FROM 
                            matches m
                        JOIN 
                            match_headers mh 
                        ON m.match_id = mh.match_id
                        JOIN venue_info v 
                            ON m.venue_name = v.ground
                        JOIN 
                            team t 
                        ON t.team_id = mh.winning_team_id
                        )x1
                    )z1
                    )v1
                    GROUP BY team_name, match_location
                    ORDER BY team_name, match_location;
                    """,
                    "13":"""
                            SELECT 
                                s1.name as player_1_name,
                                s2.name  AS player_2_name,
                                s1.innings_id,
                                (s1.runs + s2.runs) AS combined_runs
                            FROM batsmen s1
                            JOIN batsmen s2
                                ON s1.match_id = s2.match_id
                                AND s1.innings_id = s2.innings_id
                                AND s2.batting_position = s1.batting_position + 1
                            WHERE (s1.runs + s2.runs) >= 100
                            ORDER BY 
                                s1.match_id,
                                s1.innings_id,
                                s1.batting_position;
                        """,
                    "14":"""
                            WITH cleaned_bowling AS (
                                SELECT 
                                    b.bowler_id,
                                    b.name AS bowler_name,
                                    m.venue_name,
                                    b.wickets,
                                    b.economy,
                                    b.overs,
                                    b.match_id
                                FROM bowlers b
                                JOIN matches m 
                                ON b.match_id = m.match_id
                                WHERE 
                                    CASE 
                                        WHEN b.overs LIKE '%.%' THEN split_part(b.overs, '.', 1)::int
                                        ELSE b.overs::int
                                    END >= 4
                            ),

                            aggregated AS (
                                SELECT
                                    bowler_id,
                                    bowler_name,
                                    venue_name,
                                    COUNT(match_id) AS matches_played,
                                    SUM(wickets) AS total_wickets,
                                    AVG(economy) AS avg_economy
                                FROM cleaned_bowling
                                GROUP BY bowler_id, bowler_name, venue_name
                            )

                            SELECT
                                bowler_name,
                                venue_name,
                                matches_played,
                                total_wickets,
                                ROUND(avg_economy, 2) AS avg_economy
                            FROM aggregated
                            WHERE matches_played >= 3
                            ORDER BY bowler_name, venue_name;
                        """,
                        "15":"""WITH close_matches AS (
                                    SELECT
                                        m.match_id,
                                        mh.winning_team_id,
                                        mh.victory_type,
                                        mh.victory_margin
                                    FROM matches m
                                    Join 
                                        match_headers mh
                                    ON
                                        mh.match_id = m.match_id
                                    WHERE 
                                        (mh.victory_type = 'runs' AND mh.victory_margin < 50)
                                        OR
                                        (mh.victory_type = 'wickets' AND mh.victory_margin < 5)
                                ),

                                player_close_stats AS (
                                    SELECT
                                        b.batsman_id as player_id,
                                        b.name as player_name,
                                        (select t.team_id from players pl ,team t where pl.player_id = b.batsman_id and t.team_name = pl.team) as team_id,
                                        b.match_id,
                                        b.runs,
                                        cm.winning_team_id,
                                        CASE 
                                            WHEN (select t.team_id from players pl ,team t where pl.player_id = b.batsman_id and t.team_name = pl.team) = cm.winning_team_id THEN 1 
                                            ELSE 0 
                                        END AS team_won
                                    FROM batsmen b
                                    INNER JOIN close_matches cm 
                                        ON b.match_id = cm.match_id
                                    WHERE (select t.team_id from players pl ,team t where pl.player_id = b.batsman_id and t.team_name = pl.team) is not null	
                                ),

                                aggregated AS (
                                    SELECT
                                        pcs.player_id,
                                        pcs.player_name,
                                        COUNT(*) AS close_matches_played,
                                        AVG(pcs.runs) AS avg_runs_in_close_matches,
                                        SUM(pcs.team_won) AS close_matches_won_when_batted
                                    FROM player_close_stats pcs
                                    GROUP BY pcs.player_id,pcs.player_name
                                )

                                SELECT
                                    a.player_id,
                                    a.player_name,
                                    a.close_matches_played,
                                    round(a.avg_runs_in_close_matches,2) as Avg,
                                    a.close_matches_won_when_batted
                                FROM 
                                    aggregated a
                                ORDER BY 
                                    a.avg_runs_in_close_matches DESC
                                LIMIT 20;
                        """,
                        "16":"""
                            SELECT
                                b.batsman_id,
                                p.player_name,
                                EXTRACT(YEAR FROM m.match_date) AS year,
                                COUNT(*) AS matches_played,
                                round(AVG(b.runs),2) AS avg_runs_per_match,
                                round(AVG(b.strike_rate),2) AS avg_strike_rate
                            FROM batsmen b
                            JOIN matches m
                                ON m.match_id = b.match_id
                            JOIN players p
                                ON p.player_id = b.batsman_id
                            WHERE EXTRACT(YEAR FROM m.match_date) >= 2020
                            GROUP BY
                                b.batsman_id,
                                p.player_name,
                                EXTRACT(YEAR FROM m.match_date)
                            HAVING COUNT(*) >= 5
                            ORDER BY
                                b.batsman_id,
                                year;
                            """,
                        "17":"""
                                SELECT
                                    toss_decision,
                                    COUNT(*) AS total_toss_won,
                                    SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) 
                                        AS toss_and_match_won,
                                    ROUND(
                                        SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END)::numeric 
                                        / COUNT(*) * 100, 2
                                    ) AS win_percentage
                                FROM match_headers
                                WHERE toss_decision <> ''
                                GROUP BY toss_decision
                                ORDER BY toss_decision;
                            """,
                        "18":"""

                            WITH cleaned_bowling AS (
                                SELECT
                                    b.bowler_id,
                                    b.match_id,
                                    CAST(b.overs AS numeric) AS overs_bowled,
                                    b.runs,
                                    b.wickets
                                FROM bowlers b
                                WHERE b.overs IS NOT NULL
                            ),

                            limited_overs_matches AS (
                                SELECT match_id, match_format
                                FROM matches
                                WHERE match_format IN ('ODI', 'T20I')
                            ),
                            bowler_stats AS (
                                SELECT
                                    cb.bowler_id,
                                    COUNT(DISTINCT cb.match_id) AS matches_played,
                                    SUM(cb.overs_bowled) AS total_overs,
                                    SUM(cb.runs) AS total_runs,
                                    SUM(cb.wickets) AS total_wickets
                                FROM cleaned_bowling cb
                                JOIN limited_overs_matches m
                                    ON m.match_id = cb.match_id
                                GROUP BY cb.bowler_id
                            ),
                            filtered_bowlers AS (
                                SELECT
                                    bowler_id,
                                    p.player_name as bowler_name,
                                    matches_played,
                                    total_overs,
                                    total_runs,
                                    total_wickets,
                                    (total_overs / matches_played) AS avg_overs_per_match
                                FROM bowler_stats
                                JOIN players p
                                ON player_id = bowler_id
                                WHERE matches_played >= 10
                            )

                            SELECT
                                fb.bowler_id,
                                fb.bowler_name,
                                fb.matches_played,
                                fb.total_wickets,
                                ROUND(fb.total_runs / fb.total_overs, 2) AS overall_economy,
                                ROUND(fb.avg_overs_per_match, 2) AS avg_overs_per_match
                            FROM filtered_bowlers fb
                            WHERE fb.avg_overs_per_match >= 2       
                            ORDER BY overall_economy ASC;  
                            """,
                        "19":"""
                                WITH filtered_innings AS (
                                    SELECT
                                        b.batsman_id,
                                        b.runs,
                                        b.balls,
                                        m.match_date
                                    FROM batsmen b
                                    JOIN matches m
                                        ON m.match_id = b.match_id
                                    WHERE b.balls >= 10                     
                                    AND m.match_date >= '2022-01-01'
                                ),

                                player_stats AS (
                                    SELECT
                                        batsman_id,
                                        COUNT(*) AS innings_played,
                                        AVG(runs) AS avg_runs,
                                        STDDEV(runs) AS run_stddev
                                    FROM filtered_innings
                                    GROUP BY batsman_id
                                )
                                SELECT
                                    ps.batsman_id as batsman_id,
                                    (SELECT name from batsmen where batsman_id = ps.batsman_id limit 1 ) as player_name,
                                    ps.innings_played as innings_played,
                                    ROUND(ps.avg_runs, 2) AS average_runs,
                                    ROUND(ps.run_stddev, 2) AS run_stddev
                                FROM player_stats ps
                                WHERE innings_played >= 1
                                    AND run_stddev is not null
                                ORDER BY run_stddev ASC;
                            """,
                        "20":"""
                            WITH batsman_with_format AS (
                                SELECT
                                    b.batsman_id,
                                    b.name AS player_name,
                                    m.match_format,
                                    m.match_id,
                                    b.runs
                                FROM batsmen b
                                JOIN matches m
                                    ON m.match_id = b.match_id
                            ),

                            format_stats AS (
                                SELECT
                                    batsman_id,
                                    player_name,
                                    match_format,
                                    COUNT(DISTINCT match_id) AS matches_played,
                                    AVG(runs) AS batting_average
                                FROM batsman_with_format
                                GROUP BY batsman_id, player_name, match_format
                            ),

                            pivoted AS (
                                SELECT
                                    batsman_id,
                                    player_name,
                                    SUM(CASE WHEN match_format = 'TEST' THEN matches_played ELSE 0 END) AS test_matches,
                                    SUM(CASE WHEN match_format = 'ODI' THEN matches_played ELSE 0 END) AS odi_matches,
                                    SUM(CASE WHEN match_format = 'T20' THEN matches_played ELSE 0 END) AS t20_matches,
                                    AVG(CASE WHEN match_format = 'TEST' THEN batting_average END) AS test_avg,
                                    AVG(CASE WHEN match_format = 'ODI' THEN batting_average END) AS odi_avg,
                                    AVG(CASE WHEN match_format = 'T20' THEN batting_average END) AS t20_avg
                                FROM format_stats
                                GROUP BY batsman_id, player_name
                            )

                            SELECT 
                                batsman_id,
                                    player_name,
                                    test_matches,
                                    odi_matches,
                                    t20_matches,
                                    coalesce(round(test_avg,2),0.0) as Test_Avg,
                                    coalesce(round(odi_avg,2),0.0) as ODI_Avg,
                                    coalesce(round(t20_avg,2),0.0) as T20_Avg
                            FROM pivoted
                            WHERE (test_matches + odi_matches + t20_matches) >= 20
                            ORDER BY (test_matches + odi_matches + t20_matches) DESC;
                            """,
                        "21":"""
                        WITH batting AS (
                                SELECT
                                    b.batsman_id,
                                    b.name AS player_name,
                                    SUM(b.runs) AS total_runs,
                                    ROUND(AVG(b.runs),2) AS batting_avg,
                                    ROUND(AVG(b.strike_rate),2) AS avg_sr
                                FROM batsmen b
                                JOIN matches m ON m.match_id = b.match_id
                                GROUP BY b.batsman_id, b.name
                            ),
                            bowling AS (
                                SELECT
                                    bo.bowler_id AS player_id,
                                    bo.name AS player_name,
                                    SUM(bo.wickets) AS total_wkts,
                                    ROUND(AVG(bo.wickets),2) AS bowl_avg,
                                    ROUND(SUM(runs)/SUM(overs::NUMERIC),2) AS econ_rate
                                FROM bowlers bo
                                JOIN matches m ON m.match_id = bo.match_id
                                GROUP BY bo.bowler_id,bo.name
                            ),
                            fielding AS (
                                SELECT 
                                    ps.player_id,
                                    x1.player_name,
                                    x1.catches as total_catches,
                                    x1.stumpings as total_stumpings
                                FROM
                                (SELECT
                                        x.fielder_name as player_name,
                                        SUM(x.catches) AS catches,
                                        SUM(x.stumpings) AS stumpings
                                    FROM (
                                        SELECT 
                                            INITCAP(regexp_replace(out_desc,'c[[:space:]]+(?:\\(sub\\)[[:space:]]*)?((?:[^[:space:]]+[[:space:]]*){1,3})[[:space:]]+b[[:space:]].*$','\\1','i')) AS fielder_name,
                                            1 AS catches,
                                            0 AS stumpings
                                        FROM batsmen
                                        WHERE out_desc ~* 'c[[:space:]]+'
                                        AND out_desc   ~* 'b[[:space:]]+'
                                        AND out_desc  !~* 'st[[:space:]]+'
                                        UNION ALL
                                        SELECT
                                            INITCAP(regexp_replace(out_desc,'st[[:space:]]+(?:\\(sub\\)[[:space:]]*)?((?:[^[:space:]]+[[:space:]]*){1,3})[[:space:]]+b[[:space:]].*$','\\1','i')) AS fielder_name,
                                           0 AS catches,
                                            1 AS stumpings
                                        FROM batsmen
                                        WHERE out_desc ~* 'st[[:space:]]+'
                                        AND out_desc ~* 'b[[:space:]]+'
                                       
                                    ) AS x
                                    GROUP BY fielder_name
                                    ORDER BY catches DESC, stumpings DESC)x1,players ps 
                                    WHERE ps.player_name = x1.player_name
                            ),
                            combined AS (
                                SELECT
                                    COALESCE(b.batsman_id, bo.player_id, f.player_id) AS player_id,
                                    COALESCE(b.player_name, bo.player_name, f.player_name) AS player_name,
                                    COALESCE(b.total_runs, 0) AS total_runs,
                                    COALESCE(b.batting_avg, 0) AS batting_avg,
                                    COALESCE(b.avg_sr, 0) AS strike_rate,
                                    COALESCE(bo.total_wkts, 0) AS wickets,
                                    COALESCE(bo.bowl_avg, 50) AS bowl_avg,
                                    COALESCE(bo.econ_rate, 6) AS econ_rate,
                                    COALESCE(f.total_catches, 0) AS catches,
                                    COALESCE(f.total_stumpings, 0) AS stumpings
                                FROM batting b
                                FULL OUTER JOIN bowling bo
                                    ON b.batsman_id = bo.player_id
                                FULL OUTER JOIN fielding f
                                    ON COALESCE(b.batsman_id, bo.player_id) = f.player_id
                            ),
                            final_scores AS (
                                SELECT
                                    player_id,
                                    player_name,
                                    ((total_runs * 0.01)+(batting_avg * 0.5)+(strike_rate * 0.3)) AS batting_points,
                                    ((wickets * 2)+ ((50 - bowl_avg) * 0.5)+ ((6 - econ_rate) * 2)) AS bowling_points,
                                    ((catches * 1) + (stumpings * 2)) AS fielding_points
                                FROM combined
                            )
                            SELECT
                                player_id,
                                player_name,
                                round(batting_points,2) as batting_points,
                                round(bowling_points,2) as bowling_points,
                                round(fielding_points,2) as fielding_points,
                                round((batting_points + bowling_points + fielding_points),2) AS total_score
                            FROM final_scores
                            ORDER BY  total_score DESC;
                              """,
                        "22":"""
                                WITH recent_matches AS (
                                    SELECT 
                                        m.match_id,
                                        m.team_1_name as team_a,
                                        m.team_2_name as team_b,
                                        m.venue_name,
                                        m.match_date,
                                        mh.winning_team_id,
                                        (SELECT team_name FROM team where team_id = mh.winning_team_id) as winner_name,
                                        mh.toss_winner_name,
                                        mh.toss_decision,
                                        mh.victory_type,
                                        mh.victory_margin
                                    FROM matches m
                                    JOIN match_headers mh ON mh.match_id = m.match_id
                                    WHERE m.match_date >= CURRENT_DATE - INTERVAL '3 years'
                                ),
                                pair_counts AS (
                                    SELECT 
                                        team_a, team_b,
                                        COUNT(*) AS total_matches
                                    FROM recent_matches
                                    GROUP BY team_a, team_b
                                    HAVING COUNT(*) >= 5
                                ),
                                pair_data AS (
                                    SELECT 
                                        r.*,
                                        pc.total_matches
                                    FROM recent_matches r
                                    JOIN pair_counts pc 
                                    ON pc.team_a = r.team_a AND pc.team_b = r.team_b
                                ),
                                aggregated AS (
                                SELECT 
                                    team_a,
                                    team_b,

                                    ROUND(COALESCE(COUNT(*), 0)::numeric) AS total_matches,
                                    ROUND(COALESCE(SUM(CASE WHEN lower(winner_name) = lower(team_a) THEN 1 ELSE 0 END), 0)::numeric) 
                                        AS team_a_wins,
                                    ROUND(COALESCE(SUM(CASE WHEN lower(winner_name) = lower(team_b) THEN 1 ELSE 0 END), 0)::numeric) 
                                        AS team_b_wins,
                                    ROUND(
                                        COALESCE(
                                            100.0 * SUM(CASE WHEN lower(winner_name) = lower(team_a) THEN 1 ELSE 0 END) 
                                            / NULLIF(COUNT(*), 0), 
                                        0)::numeric,2) AS team_a_win_pct,
                                    ROUND(
                                        COALESCE(
                                            100.0 * SUM(CASE WHEN lower(winner_name) = lower(team_b) THEN 1 ELSE 0 END) 
                                            / NULLIF(COUNT(*), 0), 
                                        0)::numeric, 
                                    2) AS team_b_win_pct,
                                    ROUND(
                                        COALESCE(
                                            AVG(CASE 
                                                    WHEN lower(winner_name) = lower(team_a) 
                                                        AND victory_type = 'runs' 
                                                    THEN victory_margin 
                                                END),
                                        0)::numeric,2) AS team_a_avg_win_runs,
                                    ROUND(
                                        COALESCE(
                                            AVG(CASE 
                                                    WHEN lower(winner_name) = lower(team_b) 
                                                        AND victory_type = 'runs' 
                                                    THEN victory_margin 
                                                END),
                                        0)::numeric,2) AS team_b_avg_win_runs,

                                    ROUND(
                                        COALESCE(
                                            AVG(CASE 
                                                    WHEN lower(winner_name) = lower(team_a) 
                                                        AND victory_type = 'wickets' 
                                                    THEN victory_margin 
                                                END),
                                        0)::numeric,2) AS team_a_avg_win_wkts,

                                    ROUND(
                                        COALESCE(
                                            AVG(CASE 
                                                    WHEN lower(winner_name) = lower(team_b) 
                                                        AND victory_type = 'wickets' 
                                                    THEN victory_margin 
                                                END),
                                        0)::numeric,2) AS team_b_avg_win_wkts

                                FROM pair_data
                                GROUP BY team_a, team_b

                                ),

                                venue_perf AS (
                                    SELECT 
                                    team_a,
                                    team_b,
                                    venue_name,

                                    ROUND(COALESCE(COUNT(*), 0)::numeric) AS matches_at_venue,

                                    ROUND(COALESCE(SUM(CASE WHEN lower(winner_name) = lower(team_a) THEN 1 ELSE 0 END), 0)::numeric) 
                                        AS team_a_wins_venue,

                                    ROUND(COALESCE(SUM(CASE WHEN lower(winner_name) = lower(team_b) THEN 1 ELSE 0 END), 0)::numeric) 
                                        AS team_b_wins_venue,

                                    ROUND(COALESCE(SUM(
                                        CASE 
                                            WHEN lower(toss_winner_name) = lower(team_a)
                                                AND toss_decision = 'Batting'
                                                AND lower(winner_name) = lower(team_a)
                                            THEN 1 
                                        END
                                    ), 0)::numeric) AS team_a_win_bat_first,

                                    ROUND(COALESCE(SUM(
                                        CASE 
                                            WHEN lower(toss_winner_name) = lower(team_b)
                                                AND toss_decision = 'Batting'
                                                AND lower(winner_name) = lower(team_b)
                                            THEN 1 
                                        END
                                    ), 0)::numeric) AS team_b_win_bat_first,

                                    ROUND(COALESCE(SUM(
                                        CASE 
                                            WHEN lower(toss_winner_name) = lower(team_a)
                                                AND toss_decision = 'Bowling'
                                                AND lower(winner_name) = lower(team_a)
                                            THEN 1 
                                        END
                                    ), 0)::numeric) AS team_a_win_bowl_first,

                                    ROUND(COALESCE(SUM(
                                        CASE 
                                            WHEN lower(toss_winner_name) = lower(team_b)
                                                AND toss_decision = 'Bowling'
                                                AND lower(winner_name) = lower(team_b)
                                            THEN 1 
                                        END
                                    ), 0)::numeric) AS team_b_win_bowl_first

                                FROM pair_data
                                GROUP BY team_a, team_b, venue_name
                                )

                                SELECT 
                                    a.*,
                                    vp.venue_name,
                                    vp.matches_at_venue,
                                    vp.team_a_wins_venue,
                                    vp.team_b_wins_venue,
                                    vp.team_a_win_bat_first,
                                    vp.team_b_win_bat_first,
                                    vp.team_a_win_bowl_first,
                                    vp.team_b_win_bowl_first
                                FROM aggregated a
                                LEFT JOIN venue_perf vp
                                ON a.team_a = vp.team_a 
                                    AND a.team_b = vp.team_b
                                ORDER BY a.total_matches DESC; 
                            """,
                        "23":"""
                                    WITH bats_with_date AS (
                                        SELECT
                                            b.*, 
                                            m.match_date
                                        FROM batsmen b
                                        JOIN matches m ON m.match_id = b.match_id
                                        ),
                                        ranked_innings AS (
                                        SELECT
                                            bwd.*,
                                            ROW_NUMBER() OVER (
                                            PARTITION BY bwd.batsman_id
                                            ORDER BY bwd.match_date DESC, bwd.match_id DESC
                                            ) AS rn
                                        FROM bats_with_date bwd
                                        ),

                                        last10 AS (
                                        SELECT *
                                        FROM ranked_innings
                                        WHERE rn <= 10
                                        ),
                                        players_with_10 AS (
                                        SELECT batsman_id
                                        FROM batsmen
                                        GROUP BY batsman_id
                                        HAVING COUNT(*) >= 10
                                        ),
                                        player_recent AS (
                                        SELECT
                                            l.batsman_id,
                                            l.name AS player_name,

                                            -- counts
                                            COALESCE(COUNT(*) FILTER (WHERE rn <= 10), 0)::numeric AS matches_in_last_10,

                                            -- averages runs last10 & last5
                                            ROUND(COALESCE(AVG(runs) FILTER (WHERE rn <= 10), 0)::numeric, 2) AS avg_runs_last10,
                                            ROUND(COALESCE(AVG(runs) FILTER (WHERE rn <= 5), 0)::numeric, 2)  AS avg_runs_last5,
                                            ROUND(COALESCE(AVG(strike_rate) FILTER (WHERE rn <= 10), 0)::numeric, 2) AS avg_sr_last10,
                                            ROUND(COALESCE(AVG(strike_rate) FILTER (WHERE rn <= 5), 0)::numeric, 2)  AS avg_sr_last5,
                                            ROUND(
                                            COALESCE(AVG(strike_rate) FILTER (WHERE rn <= 5), 0)
                                            - COALESCE(AVG(strike_rate) FILTER (WHERE rn <= 10), 0)
                                            , 2) AS sr_trend,

                                            
                                            ROUND(COALESCE(SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END), 0)::numeric, 2) AS scores_ge_50_last10,
                                            ROUND(COALESCE(STDDEV_SAMP(runs), 0)::numeric, 2) AS run_stddev_last10

                                        FROM last10 l
                                        JOIN players_with_10 p ON p.batsman_id = l.batsman_id
                                        GROUP BY l.batsman_id, l.name
                                        )

                                        -- final scoring and categorization
                                        SELECT
                                        pr.batsman_id,
                                        pr.player_name,
                                        pr.matches_in_last_10,
                                        pr.avg_runs_last5,
                                        pr.avg_runs_last10,
                                        pr.avg_sr_last5,
                                        pr.avg_sr_last10,
                                        pr.sr_trend,
                                        pr.scores_ge_50_last10,
                                        pr.run_stddev_last10,
                                        ROUND(
                                            (
                                            (pr.avg_runs_last5 * 0.55)     
                                            + (pr.sr_trend * 0.25)         
                                            - (pr.run_stddev_last10 * 0.20)
                                            + (pr.scores_ge_50_last10 * 1.5)
                                            )
                                        , 2) AS form_score,
                                        CASE
                                            WHEN pr.avg_runs_last5 >= 50
                                            AND pr.avg_runs_last5 >= pr.avg_runs_last10 * 1.25
                                            AND pr.sr_trend >= 5
                                            AND pr.run_stddev_last10 <= 10
                                            THEN 'Excellent Form'

                                            WHEN pr.avg_runs_last5 >= 30
                                            OR pr.scores_ge_50_last10 >= 2
                                            THEN 'Good Form'

                                            WHEN pr.avg_runs_last5 >= pr.avg_runs_last10 * 0.95
                                            THEN 'Average Form'

                                            ELSE 'Poor Form'
                                        END AS form_category

                                        FROM player_recent pr
                                        ORDER BY form_score DESC, pr.matches_in_last_10 DESC, pr.player_name;

                            """,
                        "24": """
                                WITH pair_stats AS (
                                    SELECT
                                        match_id,
                                        bat1_name AS player_a,
                                        bat2_name AS player_b,
                                        total_runs,
                                        (CASE WHEN total_runs > 50 THEN 1 ELSE 0 END) AS good_partnership
                                    FROM partnerships
                                )
                                SELECT
                                    player_a AS batsman_1,
                                    player_b AS batsman_2,
                                    COUNT(*) AS total_partnerships,
                                    ROUND(AVG(total_runs),2) AS avg_partnership_runs,
                                    SUM(CASE WHEN total_runs > 50 THEN 1 ELSE 0 END) AS fifty_plus_partnerships,
                                    MAX(total_runs) AS highest_partnership,
                                    ROUND(SUM(good_partnership)::DECIMAL / COUNT(*) * 100,2) AS success_rate
                                FROM pair_stats
                                GROUP BY player_a, player_b
                                HAVING COUNT(*) >= 5
                                ORDER BY success_rate DESC, avg_partnership_runs DESC;
                            """,
                        "25": """
                               WITH bats_with_date AS (
                                SELECT
                                    b.batsman_id,
                                    m.match_date,
                                    m.match_id,
                                    b.runs,
                                    b.strike_rate
                                FROM batsmen b
                                JOIN matches m ON m.match_id = b.match_id
                                ),

                                quarterly AS (
                                SELECT
                                    batsman_id,
                                    date_trunc('quarter', match_date) AS quarter_start,
                                    COUNT(DISTINCT match_id) AS matches_in_quarter,
                                    AVG(runs) AS avg_runs,
                                    AVG(strike_rate) AS avg_sr
                                FROM bats_with_date
                                GROUP BY batsman_id,date_trunc('quarter', match_date)
                                ),
                                quarterly_filtered AS (
                                SELECT *
                                FROM quarterly
                                WHERE matches_in_quarter >= 3
                                ),
                                player_quarter_counts AS (
                                SELECT
                                    batsman_id,
                                    COUNT(*) AS quarters_count
                                FROM quarterly_filtered
                                GROUP BY batsman_id
                                HAVING COUNT(*) >= 6
                                ),
                                player_quarters_indexed AS (
                                SELECT
                                    qf.batsman_id,
                                    (SELECT player_name FROM players WHERE player_id = qf.batsman_id) as player_name,
                                    qf.quarter_start,
                                    qf.matches_in_quarter,
                                    ROUND(COALESCE(qf.avg_runs, 0)::numeric, 4) AS avg_runs,
                                    ROUND(COALESCE(qf.avg_sr, 0)::numeric, 4) AS avg_sr,
                                    ROW_NUMBER() OVER (PARTITION BY qf.batsman_id ORDER BY qf.quarter_start) AS q_index
                                FROM quarterly_filtered qf
                                JOIN player_quarter_counts pc
                                    ON pc.batsman_id = qf.batsman_id
                                ),

                                quarterly_trends AS (
                                SELECT
                                    pq.batsman_id,
                                    pq.player_name,
                                    pq.quarter_start,
                                    pq.q_index,
                                    pq.matches_in_quarter,
                                    pq.avg_runs,
                                    pq.avg_sr,

                                    LAG(pq.avg_runs) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) AS prev_avg_runs,
                                    LAG(pq.avg_sr)   OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) AS prev_avg_sr,
                                    CASE
                                    WHEN LAG(pq.avg_runs) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) IS NULL THEN NULL
                                    WHEN LAG(pq.avg_runs) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) = 0 THEN NULL
                                    ELSE (pq.avg_runs - LAG(pq.avg_runs) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index))
                                            / LAG(pq.avg_runs) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index)
                                    END AS pct_change_runs,

                                    CASE
                                    WHEN LAG(pq.avg_sr) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) IS NULL THEN NULL
                                    WHEN LAG(pq.avg_sr) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index) = 0 THEN NULL
                                    ELSE (pq.avg_sr - LAG(pq.avg_sr) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index))
                                            / LAG(pq.avg_sr) OVER (PARTITION BY pq.batsman_id ORDER BY pq.q_index)
                                    END AS pct_change_sr

                                FROM player_quarters_indexed pq
                                ),
                                quarterly_classified AS (
                                SELECT
                                    qt.*,
                                    CASE
                                    WHEN qt.pct_change_runs IS NULL AND qt.pct_change_sr IS NULL THEN 'BaseQuarter'
                                    WHEN (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs >= 0.05)
                                        AND (qt.pct_change_sr IS NOT NULL AND qt.pct_change_sr >= 0.05)
                                        THEN 'Improving'
                                    WHEN (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs <= -0.05)
                                        AND (qt.pct_change_sr IS NOT NULL AND qt.pct_change_sr <= -0.05)
                                        THEN 'Declining'
                                    WHEN ( (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs >= 0.05) OR
                                            (qt.pct_change_sr  IS NOT NULL AND qt.pct_change_sr  >= 0.05) )
                                        AND NOT ( (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs <= -0.05) OR
                                                (qt.pct_change_sr  IS NOT NULL AND qt.pct_change_sr  <= -0.05) )
                                        THEN 'Improving'
                                    WHEN ( (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs <= -0.05) OR
                                            (qt.pct_change_sr  IS NOT NULL AND qt.pct_change_sr  <= -0.05) )
                                        AND NOT ( (qt.pct_change_runs IS NOT NULL AND qt.pct_change_runs >= 0.05) OR
                                                (qt.pct_change_sr  IS NOT NULL AND qt.pct_change_sr  >= 0.05) )
                                        THEN 'Declining'
                                    ELSE 'Stable'
                                    END AS quarter_label
                                FROM quarterly_trends qt
                                ),
                                player_quarter_summary AS (
                                SELECT
                                    qc.batsman_id,
                                    qc.player_name,
                                    COUNT(*) FILTER (WHERE qc.quarter_label IS NOT NULL AND qc.quarter_label <> 'BaseQuarter') AS compared_quarters_count,
                                    COUNT(*) FILTER (WHERE qc.quarter_label = 'Improving') AS improving_count,
                                    COUNT(*) FILTER (WHERE qc.quarter_label = 'Declining')  AS declining_count,
                                    COUNT(*) FILTER (WHERE qc.quarter_label = 'Stable')    AS stable_count,
                                    ROUND(COALESCE(AVG(qc.avg_runs),0)::numeric, 2) AS mean_quarterly_runs,
                                    ROUND(COALESCE(AVG(qc.avg_sr),0)::numeric, 2)   AS mean_quarterly_sr
                                FROM quarterly_classified qc
                                GROUP BY qc.batsman_id, qc.player_name
                                ),
                                player_regression AS (
                                SELECT
                                    pq.batsman_id,
                                    pq.player_name,
                                    COALESCE(regr_slope(avg_runs, q_index) , 0) AS slope_runs,
                                    COALESCE(regr_slope(avg_sr, q_index)   , 0) AS slope_sr
                                FROM player_quarters_indexed pq
                                GROUP BY pq.batsman_id, pq.player_name
                                ),
                                player_trajectory AS (
                                SELECT
                                    ps.batsman_id,
                                    ps.player_name,
                                    ps.compared_quarters_count,
                                    ps.improving_count,
                                    ps.declining_count,
                                    ps.stable_count,
                                    ps.mean_quarterly_runs,
                                    ps.mean_quarterly_sr,
                                    pr.slope_runs,
                                    pr.slope_sr,
                                    ROUND(COALESCE( (ps.improving_count::numeric / NULLIF(ps.compared_quarters_count,0)) * 100, 0)::numeric, 2) AS pct_quarters_improving,
                                    ROUND(COALESCE( (ps.declining_count::numeric  / NULLIF(ps.compared_quarters_count,0)) * 100, 0)::numeric, 2) AS pct_quarters_declining,
                                    CASE
                                    WHEN pr.slope_runs > 0 AND (ps.improving_count::numeric / NULLIF(ps.compared_quarters_count,0)) >= 0.60 THEN 'Career Ascending'
                                    WHEN pr.slope_runs < 0 AND (ps.declining_count::numeric  / NULLIF(ps.compared_quarters_count,0)) >= 0.60 THEN 'Career Declining'
                                    ELSE 'Career Stable'
                                    END AS career_phase

                                FROM player_quarter_summary ps
                                JOIN player_regression pr ON pr.batsman_id = ps.batsman_id
                                )

                                SELECT
                                pqc.batsman_id,
                                pqc.player_name,
                                pqc.quarter_start,
                                ROUND(pqc.avg_runs::numeric, 2) AS avg_runs,
                                ROUND(pqc.avg_sr::numeric, 2)   AS avg_sr,
                                pqc.matches_in_quarter,
                                ROUND(COALESCE(pqc.pct_change_runs * 100, 0)::numeric, 2) AS pct_change_runs,
                                ROUND(COALESCE(pqc.pct_change_sr * 100, 0)::numeric, 2)   AS pct_change_sr,
                                pqc.quarter_label,

                                pt.compared_quarters_count,
                                pt.improving_count,
                                pt.declining_count,
                                pt.stable_count,
                                pt.pct_quarters_improving,
                                pt.pct_quarters_declining,
                                pt.mean_quarterly_runs,
                                pt.mean_quarterly_sr,
                                ROUND(pt.slope_runs::numeric, 6) AS slope_runs,
                                ROUND(pt.slope_sr::numeric, 6)  AS slope_sr,
                                pt.career_phase

                                FROM (
                                SELECT
                                    qc.batsman_id,
                                    qc.player_name,
                                    qc.quarter_start,
                                    qc.matches_in_quarter,
                                    qc.avg_runs,
                                    qc.avg_sr,
                                    qc.pct_change_runs,
                                    qc.pct_change_sr,
                                    qc.quarter_label
                                FROM quarterly_classified qc
                                ) pqc
                                JOIN player_trajectory pt ON pt.batsman_id = pqc.batsman_id
                                ORDER BY pqc.player_name, pqc.quarter_start;
                            """
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
    st.code(f"""{query_table.get(selected_qid)}""",language="sql")
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
