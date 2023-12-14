import requests
import sys
from pyfiglet import Figlet

# Project Name: SIGHTSTONE
# Lex Lei
# Boston, MA
# U.S.A

# Constants
API_KEY = 'RGAPI-b12d0f41-21ee-4ae9-8cc2-1007e966fb58' # Riot Games API Key
CLIENT_VER = "13.24.1" # League of Legends Client version
RESPONSE_ERRORS = { # Dictionary mapping HTTP response codes to error descriptions
    400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden',
    404: 'Data Not Found', 405: 'Method Not Allowed',
    415: 'Unsupported Media Type', 429: 'Rate Limit Exceeded',
    500: 'Internal Server Error', 502: 'Bad Gateway',
    503: 'Service Unavailable', 504: 'Gateway Timeout'
}

class Participant:
    """
    Represents a participant in a League of Legends match.

    Attributes:
        participant (dict): Dictionary containing participant information.
        sid (str): Summoner ID of the participant.
        name (str): Summoner name of the participant.
        team (int): Team ID of the participant.
        cid (int): Champion ID of the participant.
        puuid (str): PUUID (Portable Unique ID) of the participant.
        rank (str): Rank of the participant in the League of Legends ranked system.
        champ_name (str): Name of the champion played by the participant.
        champ_mastery (dict): Dictionary containing participant's champion mastery information.
        winrate (float or str): Winrate of the participant if available, else "Not enough data."

    Methods:
        __init__(self, participant): Initializes a Participant object with information from a match participant.
        __str__(self): Returns a formatted string representation of the Participant object.
        get_rank(self, resp): Retrieves the player's rank from the given response.
        get_champ_name(self): Retrieves the name of the champion played by the participant.
        get_champ_mastery(self): Retrieves the participant's champion mastery information.
        get_winrate(self, resp): Calculates the winrate of the participant from the given response.
    """
    def __init__(self, participant):
        """
        Initializes a Participant object with information from a match participant.

        Args:
            participant (dict): Dictionary containing participant information.
        """
        self.participant = participant
        self.sid = participant['summonerId']
        self.name = participant['summonerName']
        self.team = participant['teamId']
        self.cid = participant['championId']
        self.puuid = participant['puuid']
        url = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.sid}'
        error, resp = request_url(url)
        self.rank = self.get_rank(resp)
        self.champ_name = self.get_champ_name()
        self.champ_mastery = self.get_champ_mastery()
        self.winrate = self.get_winrate(resp)

    def __str__(self):
        """
        Returns a formatted string representation of the Participant object.

        Returns:
            str: Formatted string with participant information.
        """
        top_champ = ''
        if 0 < self.champ_mastery['top'] <= 5:
            top_champ = f"This is {self.name}'s #{self.champ_mastery['top']} champion"
        return (f'Summoner: {self.name:<18} Rank: {self.rank:<15} Winrate: {self.winrate:<3}%   Champion: {self.champ_name:<15}'
        f'Mastery Level: {self.champ_mastery['level']:<4} Points: {self.champ_mastery['points']:<10} {top_champ}')

    # retrieve player rank
    def get_rank(self, resp):
        """
        Retrieves the player's rank from the given response.

        Args:
            resp (list): List containing player's rank information.

        Returns:
            str: Player's rank or "UNRANKED" if no rank is found.
        """
        if len(resp) == 0:
            return "UNRANKED"
        else:
            return resp[0]['tier']

    # retrieve the champion name
    def get_champ_name(self):
        """
        Retrieves the name of the champion played by the participant.

        Returns:
            str: Name of the champion.
        """
        champions = requests.get('https://ddragon.leagueoflegends.com/cdn/'+CLIENT_VER+'/data/en_US/champion.json')
        resp = champions.json()
        champion = next((champion for champion in resp['data'].values() if champion['key'] == str(self.cid)), None)
        return champion['name']

    # retrieve the participant's champion mastery information
    def get_champ_mastery(self):
        """
        Retrieves the participant's champion mastery information.

        Returns:
            dict: Dictionary with participant's champion mastery details.
        """
        level = 0
        points = 0
        top = 0
        mbs_url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.sid}/by-champion/{self.cid}?api_key={API_KEY}'
        champ_mastery_req = requests.get(mbs_url)
        mastery_resp = champ_mastery_req.json()
        if champ_mastery_req.status_code != 200:
            return {'level': level, 'points': points, 'top': top} #returns dictionary with default mastery
        else:
            level = mastery_resp['championLevel']
            points = mastery_resp['championPoints']
            url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.puuid}/top?count=5&api_key={API_KEY}' #gets top 5 played champions
            top_champ_resp = requests.get(url)
            resp_info = top_champ_resp.json()
            for c in resp_info:
                if c['championId'] == self.cid:
                    top = resp_info.index(c)+1
                    break
            return {'level': level, 'points': points, 'top': top} #returns dictionary with participant's champion mastery

    # calculates the winrate of the participant
    def get_winrate(self, resp):
        """
        Calculates the winrate of the participant from the given response.

        Args:
            resp (list): List containing player's match history.

        Returns:
            float or str: Calculated winrate or "Not enough data" if no match history is found.
        """
        if len(resp) == 0:
            return "Not enough data"
        else:
            wins = 0
            losses = 0
            for e in resp:
                wins += e['wins']
                losses += e['losses']
            return round((wins / (losses + wins)) * 100, 1)

# main function
def main():
    """
    Main function to execute the Sightstone program.

    This function orchestrates the execution of the Sightstone program, which retrieves and displays
    game data for a League of Legends summoner.

    1. Prints the program title using the Figlet library.
    2. Prompts the user to enter a summoner name to get game data.
    3. Calls the get_player_info function to retrieve information about the entered summoner.
    4. If the summoner information is successfully obtained, proceeds to retrieve current match data.
    5. Prints a loading message while waiting for data retrieval.
    6. Calls the current_match function to get information about the current match.
    7. Calls the match_insights function to extract and display information about each participant in the match.
    8. Prints detailed information about each participant, categorizing them into "BLUE TEAM" and "RED TEAM."

    Note: The `Figlet` library is used to print an ASCII art title for the program.

    Returns:
        None
    """
    title = Figlet(font='big')
    print(title.renderText('WELCOME TO SIGHTSTONE')) #prints program title
    player_info = {}
    status = True
    while status:
        summoner_name = input('Enter summoner name to get game data: ')
        status, player_info = get_player_info(summoner_name) #gets player info in a dictionary
    print('This may take a moment, please wait...')
    participants_info = match_insights(current_match(player_info['id']))
    counter = 0
    for p in participants_info: #prints information about each participant
        if counter == 0:
            print('\nBLUE TEAM')
        if counter == 5:
            print('___________________________________________________________________________'
                  '___________________________________________________________________________')
            print('\nRED TEAM')
        print(p)
        counter += 1

# Returns a Summoner DTO, representing a summoner
def get_player_info(summoner_name):
    """
    Retrieves summoner information from the Riot Games API.

    Args:
        summoner_name (str): The summoner name to query.

    Returns:
        tuple: A tuple containing an error indicator and summoner information.

            - If an error occurs during the API request, the first element of the tuple is True.
            - If the request is successful, the first element is False, and the second element
              is a dictionary containing summoner information.
    """
    url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    error, summoner = request_url(url + summoner_name)
    if error:
        print('Something went wrong, please try again.')
    return error, summoner

# Returns participant and champion information
def match_insights(match):
    """
    Extracts participant and champion information from a given match.

    Args:
        match (dict): The dictionary containing information about a League of Legends match.

    Returns:
        list: A list of Participant objects representing each participant in the match.
    """
    participant_info = []
    participants = match['participants']
    for participant in participants:
        p = Participant(participant)
        participant_info.append(p)
    return participant_info

# returns current match data
def current_match(sid):
    """
    Retrieves information about the current match for a summoner.

    Args:
        sid (str): Summoner ID used to query the current match.

    Returns:
        dict: A dictionary containing information about the current match.
    """
    url = "https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
    error, match = request_url(url + sid)
    if error:
        sys.exit('Player match information unable to be retrieved')
    return match

# executes HTTPS url get request
def request_url(url):
    """
    Executes an HTTPS GET request to the provided URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        tuple: A tuple containing an error indicator and the JSON response.

            - If an error occurs during the request, the first element of the tuple is True.
            - If the request is successful, the first element is False, and the second element
              is a dictionary representing the JSON response.
    """
    api_url = url + '?api_key=' + API_KEY #api url
    resp = requests.get(api_url) #get http response
    resp_info = resp.json() #turn response into json format
    status_code = resp.status_code
    error_found = response_errors(status_code)
    return error_found, resp_info # returns an error boolean and JSON response dict

# checks response errors
def response_errors(code):
    """
    Checks for errors in the HTTP response status code.

    Args:
        code (int): The HTTP response status code.

    Returns:
        bool: True if an error is found, False otherwise.
    """
    if code != 200:
        print(f"{code}: {RESPONSE_ERRORS[code]}")
        return True
    else:
        return False

if __name__ == '__main__':
    main()
