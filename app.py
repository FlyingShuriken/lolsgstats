from flask import Flask, render_template, request
from requests import get
from json import loads, load
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")
with open("champion.json", "r") as file:
    champion_list = load(file)


@app.route("/summoner", methods=["GET"])
def summoner():
    ign = request.args.get("ign")

    id_url = (str(config["API_ID"])).replace("REPLACE_IGN_HERE", ign)
    get_id = get(id_url)
    if get_id.status_code == 404:
        return render_template("summoner.html", msg="User not found!")
    id = loads(get_id.text)["accountId"]

    history_url = (str(config["API_HISTORY"])).replace(
        "REPLACE_ID_HERE", str(id))
    get_history = get(history_url)
    histories = loads(get_history.text)
    histories_list = histories['games']['games']
    histories_list.reverse()
    version = (loads(get(config["API_VERSION"]).text))["v"]
    query = {
        "name": "",
        "games": []
    }
    name = histories_list[0]['participantIdentities'][0]['player']['summonerName']
    profile_id = histories_list[0]['participantIdentities'][0]['player']['profileIcon']
    query["name"] = name

    for i in histories_list:
        champion = champion_list[str(i['participants'][0]['championId'])]
        kda = f"{i['participants'][0]['stats']['kills']}/{i['participants'][0]['stats']['deaths']}/{i['participants'][0]['stats']['assists']}"
        level = i['participants'][0]['stats']['champLevel']
        damage = i['participants'][0]['stats']['totalDamageDealtToChampions']
        win = i['participants'][0]['stats']['win']
        gold = i['participants'][0]['stats']['goldEarned']
        cs = i['participants'][0]['stats']['totalMinionsKilled']
        gameModeID = i['queueId']
        win_lose = ""
        gameModeIDS = {
            420: "RANKED",
            450: "ARAM",
            430: "NORMAL"
        }
        gameMode = "Other"

        if gameModeID in gameModeIDS.keys():
            gameMode = gameModeIDS[gameModeID]

        if win == True:
            win_lose = "Win"
        else:
            win_lose = "Lose"

        query["games"].append({
            "champion": champion,
            "mode": gameMode,
            "kda": kda,
            "level": level,
            "damage": damage,
            "gold": gold,
            "cs": cs,
            "winorlose": win_lose
        })

    return render_template("summoner.html", query=query, profile_id=profile_id, version=version)


@app.route("/querysearch")
def querysearch():
    return render_template("querysearch.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port="3000")
