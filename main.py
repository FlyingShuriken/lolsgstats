from requests import get
from json import loads

name = input("Name: ")
get_id = get(
    f"https://acs-garena.leagueoflegends.com/v1/players?name={name}&region=SG")
id = loads(get_id.text)["accountId"]
get_history = get(
    f"https://acs-garena.leagueoflegends.com/v1/stats/player_history/SG/{id}?begIndex=0&endIndex=5&")
histories = loads(get_history.text)
histories_list = histories['games']['games']
histories_list.reverse()
for i in histories_list:
    print(
        f"--------------GAMES--------------\n",
        f"GAMEMODE: {i['gameMode']}\n",
        f"K/D/A   : {i['participants'][0]['stats']['kills']}/{i['participants'][0]['stats']['deaths']}/{i['participants'][0]['stats']['assists']}\n"
        f"---------------------------------\n\n"
    )
