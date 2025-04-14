# web server that will receive POST req
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break_with

load_dotenv()

# initial Flask app
app = Flask(__name__)


# index route
@app.route("/")
def index():
    return render_template("index.html")


# process route
@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = ice_break_with(name=name)

    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    # will run on localhost:6006
    app.run(host="0.0.0.0", port="6006", debug=True)
