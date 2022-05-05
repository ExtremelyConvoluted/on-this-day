from flask import Flask, render_template
import datetime
import requests as req

date = datetime.datetime.now()
day = date.strftime("%d")
month = date.strftime("%m")


def getEvents(month, day):
    url = "https://en.wikipedia.org/api/rest_v1/feed/onthisday/selected/{}/{}".format(
        month, day)

    res = req.get(url).json()

    with open("templates/index.html", "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n")
        f.write(
            "<head>\n<link rel=\"stylesheet\" href='/static/style.css' />\n<title>On This Day - what happened today in history?</title>\n</head>\n"
        )
        f.write("<h1>On This Day</h1>\n")
        f.write("<h3>What happened today in history?</h3>")

        f.write("<ul>\n")
        for event in reversed(res["selected"]):
            f.write("\n <li> <a href=\"" +
                    event["pages"][0]["content_urls"]["desktop"]["page"] +
                    "\">" + str(event["year"]) + "</a> : " + event["text"] +
                    "</li> \n")

        f.write(
            "\n</ul>\n<a href=\"https://onthisday.shumyiyi.repl.co/extended\">Read extended version</a>\n</body>\n</html>\n"
        )

    with open("templates/extended.html", "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n")
        f.write(
            "<head>\n<link rel=\"stylesheet\" href='/static/style.css' />\n<title>On This Day - what happened today in history?</title>\n</head>\n"
        )
        f.write("<h1>On This Day</h1>\n")
        f.write("<h3>What happened today in history?</h3>")

        f.write("<ul>\n")
        for event in reversed(res["selected"]):
            f.write("\n <li> <a href=\"" +
                    event["pages"][0]["content_urls"]["desktop"]["page"] +
                    "\">" + str(event["year"]) + "</a> : " + event["text"] +
                    " " + str(event["pages"][0]["extract_html"]) + "</li> \n")

        f.write(
            "\n</ul>\n<a href=\"https://onthisday.shumyiyi.repl.co/\">Read compact version</a>\n</body>\n</html>\n"
        )


app = Flask(__name__)


@app.route('/')
def index():
    getEvents(month, day)
    return render_template("index.html")


@app.route('/extended')
def extended():
    getEvents(month, day)
    return render_template("extended.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
