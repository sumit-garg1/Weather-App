import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    default_city = 'Faridabad'
    city = default_city

    if request.method == "POST":
        city = request.form.get("city")
    
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=0daa75c9a7c1cc4449022cfdcfbfad5b"
    r = requests.get(url.format(city)).json()

    timestamp = r.get('dt', datetime.datetime.now().timestamp())
    date_time = datetime.datetime.utcfromtimestamp(timestamp).strftime('%B %d, %Y')

    weather = {
        "city": city,
        "temperature": round(r["main"]["temp"] - 273.15, 2),
        "min_temperature": round(r["main"]["temp_min"]-275, 2),
        "max_temperature": round(r["main"]["temp_max"]-270 , 2),
        "pressure": r["main"]["pressure"],
        "description": r["weather"][0]["description"],
        "timezone": r["timezone"],
        "icon": r["weather"][0]["icon"],
        "date_time": date_time,
        "humidity": r["main"]["humidity"],
        "wind": r["wind"]["speed"],
        "wind_deg": r["wind"]["deg"],
        "wind_gust": r["wind"].get("gust", "N/A")
    }

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
