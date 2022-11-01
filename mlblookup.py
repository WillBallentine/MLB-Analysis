from tkinter import N
import urllib3
import requests
import json
import sqlite3
from os import path

#project notes: each line in these top comments represents a task/idea for this project
#URL builder for requests
#SQL needs to handle when api returns multiple results
#make use of stat user input
#user system? tknter?

def sqlmanager():

    player_data_list = []
    player_stats_list = []

    for x in player_data_file:
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["created"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["name_display_first_last"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["position"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["college"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["bats"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["team_full"])) 
        player_data_list.append((player_data_file["search_player_all"]["queryResults"]["row"]["league"]))

    for x in player_stats_file:
        #still need to edit data key/search
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["created"]))
        player_stats_list.append((player_desired.title())) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["obp"])) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["rbi"])) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["bb"])) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["avg"])) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["hr"])) 
        player_stats_list.append((player_stats_file["sport_hitting_tm"]["queryResults"]["row"]["h"]))

    conn = sqlite3.connect(r"C:/Users/william.ballentine/Documents/learning python/Code Louisville/SQL/mlblookup/mlblookup.db")
    c = conn.cursor()
    c.execute('Insert into searches values (?,?,?,?,?,?,?)', player_data_list)
    c.execute('Insert into stats values (?,?,?,?,?,?,?,?)', player_stats_list)
    conn.commit()
    conn.close()
    print(c.rowcount)

def filebuilder():
    global player_data_file
    player_data_file = json.loads(open('playerinfo.json').read())
    global player_stats_file
    player_stats_file = json.loads(open('playerstats.json').read())
    sqlmanager()


def playerlookup():
    
    with open('playerinfo.json', 'w') as f:
        count = 0
        url = (f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='{active_status.upper()}'&name_part='{player_desired}%25'")
        response = requests.request("GET", url)
        player = str(response.json())
        player_quote_correct = player.replace("\'", "\"")
        player_cleaned = player_quote_correct.replace("{", "{\n")
        player_cleaned = player_cleaned.replace("}", "}\n")

        f.write(player_cleaned)
        count = count + 1
    f.close()

    player_data_file = json.loads(open('playerinfo.json').read())
    player_id = (player_data_file["search_player_all"]["queryResults"]["row"]["player_id"])


    with open('playerstats.json', 'w') as n:
        count = 0
        url2 = (f"http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='{season_type.upper()}'&season='{season_year}'&player_id='{player_id}'")
        response2 = requests.request("GET", url2)
        player_stats = str(response2.json())
        player_stats_quote_correct = player_stats.replace("\'", "\"")
        player_stats_cleaned = player_stats_quote_correct.replace("{", "{\n")
        player_stats_cleaned = player_stats_cleaned.replace("}", "}\n")

        n.write(player_stats_cleaned)
        count = count + 1
    n.close()
    filebuilder()

def main():
    global active_status
    active_status = input("Is this player current? Y or N: ")
    global player_desired 
    player_desired = input("What player would you like to look up? ")
    global stat_desired 
    stat_desired = input(f"What would you like to know about {player_desired}? ")
    global season_type
    season_type = input("What type of games do you want stats for? 'R' - Regular Season\n'S' - Spring Training\n'E' - Exhibition\n'A' - All Star Game\n'D' - Division Series\n'F' - First Round (Wild Card)\n'L' - League Championship\n'W' - World Series\nSelection: ")
    global season_year
    season_year = input("What year? ")
    playerlookup()
    #this is where I want to engage the end user. this will call the actual api portion to return the desired information

main()