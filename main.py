import requests
import math

# Nathan Pham
# 2/25/2025

# Uses Deadlock's API to find a specified player's stats

#Deadlock asset dictionaries
HERO_ID = {}
RANKS = {}

#Specified player information
PLAYER_TOTAL = []
PLAYER_RECENT = []
PLAYER_AVG_RANK = 0

def main():
    initialize_heroes()
    initialize_ranks()

    if find_info() != 0:
        sort_matches(PLAYER_TOTAL)
        sort_matches(PLAYER_RECENT)

        print_info()

#Gathers information regarding deadlock's character name assets
def initialize_heroes():
    heroes = requests.get("https://assets.deadlock-api.com/v2/heroes")
    
    if (heroes.status_code == 200):
        for hero in heroes.json():
            HERO_ID[hero["id"]] = hero["name"]
    else:
        print("Error: API not working")

#Gathers information regarding deadlock's rank title assets
def initialize_ranks():
    ranks = requests.get("https://assets.deadlock-api.com/v2/ranks")
    
    if (ranks.status_code == 200):
        for rank in ranks.json():
            RANKS[rank["tier"]] = rank["name"]
    else:
        print("Error: API not working")

#Gathers information regarding specified user ID's stats. Hero stats and rank.
def find_info():
    while 1:

        print()
        print("Enter the Player's ID (press 0 to escape)")
        ID = input()
        print()

        if ID == "0":
            print("Goodbye!")
            return 0
        
        hero_response = requests.get("https://analytics.deadlock-api.com/v2/players/" + ID + "/hero-stats")
        if (hero_response.status_code == 200):
            player = hero_response.json()

            for hero in player:
                PLAYER_TOTAL.append({"id": hero["hero_id"], "matches": hero["matches"], "wins": hero["wins"]})

        rank_response = requests.get("https://analytics.deadlock-api.com/v2/players/" + ID + "/match-history?min_match_id=31000000")
        if (rank_response.status_code == 200):
            matches = rank_response.json()
                
            temp_dict = {}
            match_count = 0
            rank_total = 0


            for match in matches:
                match_count += 1
                rank_total += (match["average_match_badge"])

                if match["hero_id"] not in temp_dict:
                    temp_dict[match["hero_id"]] = {"id": match["hero_id"], "matches": 1, "wins": match["match_result"]}
                else:
                    temp_dict[match["hero_id"]]["matches"] += 1
                    temp_dict[match["hero_id"]]["wins"] += match["match_result"]
            
            for index in temp_dict:
                PLAYER_RECENT.append(temp_dict[index])
            
            global PLAYER_AVG_RANK
            # global PLAYER_PEAK_RANK
            PLAYER_AVG_RANK = r2d(((rank_total) / match_count))
            PLAYER_AVG_RANK += (PLAYER_AVG_RANK - 10 * (sum(RANKS.keys()) / len(RANKS))) / 10 * 5

            return 1

        print("Invalid ID")

#Print information of specified player to console
def print_info():
    for value in PLAYER_TOTAL:
        print("*****  " + HERO_ID[value["id"]] + "  *****")
        print("Matches: ", value["matches"]) 
        print("Wins: ", value["wins"]) 
        print("Losses: ", (value["matches"] - value["wins"]))
        print("Win Rate: ", r2d(value["wins"] / value["matches"])) 

        print()

    rank = math.floor((PLAYER_AVG_RANK) / 10)
    if rank > len(RANKS):
        print("Estimated Rank: ", PLAYER_AVG_RANK, " Eternus+")
    else:
        print("Estimated Rank: ", PLAYER_AVG_RANK, " ", RANKS[rank])

    print()
    print("Press Enter to See Recent Stats")
    input()

    for value in PLAYER_RECENT:
        print("*****  " + HERO_ID[value["id"]] + "  *****")
        print("Matches: ", value["matches"]) 
        print("Wins: ", value["wins"]) 
        print("Losses: ", (value["matches"] - value["wins"]))
        print("Win Rate: ", r2d(value["wins"] / value["matches"])) 

        print()


# Helpers

#Round to 2 decimal places
def r2d(x): 
    return round(x * 100) / 100

#Simple Sort
def sort_matches(player):
    player.sort(key=lambda x: x["matches"])
    

main()
