# League-of-Legends-Live-Game-Insights
# SIGHTSTONE
#### Video Demo:  <https://www.youtube.com/watch?v=1t-7HCd4wuM&ab_channel=LexLei>
#### **Description**:

SIGHTSTONE is a Python program that retrieves live game data and insights for League of Legends players using the Riot Games API. The program name, SightStone, is a callback to an in-game item which allows players to place "vision wards" around the map, essentially letting allies see where the enemies are at all times. 

League of Legends is a competitive online multiplayer game in which the main game mode pits two teams of 5 in a match to destroy each other's base. Due to the sheer number of players in the game, the chances of going against the same enemy twice is incredibly unlikely. There are also >160 playable characters, called champions, that can be chosen from. Each champion has a different set of abilities and traits which necessitates unique play styles. Therefore players typically have no indicator on how their opponent compares to them in terms of skill.

The purpose of this program is to assist players in gaining insight on what they should expect when facing their opponent. It provides information about the current match, including participant details, ranks, win rates, and champion mastery. Providing this data on each participant in a match should help players infer how "good" their opponent is.

To be able to retrieve live game data from League of Legends, I used the Riot Games (parent company) API. I used a developer API key and RIOT API URLs to gain access to game and player data. Using the requests library, I was able to get http requests in json format. By using the player's summoner ID and encrypted player ID in the API URLs, I was able to see things such as champion masteries, wins and losses, and rankings.

In this project I have main Python project file (SightStone.py) where all the main code is stored. I also have a unit test file called test_project.py. In test_project.py, I test functions response_errors, request_url, and get_player_info in project.py. I also have a text file, requirements.txt, which lists the libraries that are required to be installed to run this program.

Overall, this project was able to accomplish the goal I had originally intended. However, due to the rate limit on pulling request using RIOT API (20 requests every second, and 100 requests every 2 minutes) I was not able to add as many features (API calls) as I wanted. The more information I try to pull from the API, the slower my program will run. I would have liked to include information on synergies between champions, areas to improve on, or best item builds.
