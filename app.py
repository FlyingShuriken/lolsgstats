from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/summoner", methods=["GET"])
def summoner():
    ign = request.args.get("ign")
    print(ign)
    return ign


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port="3000")
