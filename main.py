from flask import Flask, render_template
import pandas as pd, numpy as np

# render template objects to all be kept in specially named 'templates' folder,
# with this EXACT spelling

app = Flask("__name__")


@app.route("/")  # slash for default page
def home():
    return render_template("weather.html")


@app.route("/api/v1/<station>/<date>")  #note syntax for dynamic variables
def lookup(station, date):
    date = int(date)
    # can use zfill (zerofill) for strings
    df = pd.read_csv(f'data/TG_STAID000{int(station):03}.txt', skiprows=20)
    df['TG'] = df['   TG'].mask(df['   TG'] == -9999, np.nan) / 10
    temperature = str(df.loc[df['    DATE'] == date]['TG'].squeeze())
    return {'station': station, 'date': date, 'temperature': temperature}

if __name__ == '__main__':
    app.run(debug=True) #can add eg port=5001 if running multiple apps.
