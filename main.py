from flask import Flask, render_template
import pandas as pd, numpy as np
import pycountry

# render template objects to all be kept in specially named 'templates' folder,
# with this EXACT spelling

app = Flask("__name__")

table = pd.read_csv('data/stations.txt', skiprows=17)
#only show up to station 100
table.sort_values('STAID', inplace=True)
last = np.where(table.STAID == 100)[0][0]
table['Station Code'] = table['STAID'].astype(str)
table['Location'] = table['STANAME                                 '].str.strip()
#create list from country codes, then create dict to map to country name
code = table['CN'].unique().tolist()
ctrydict={}
for c in code:
    ctrydict[c] = pycountry.countries.get(alpha_2=c).name
table['Country'] = table['CN'].map(ctrydict)
cleantable = table[['Location', 'Country', 'Station Code']][:last+1]

@app.route("/")  # slash for default page
def home():
    cleantable = cleantable.to_html(index=False)
    return render_template("weather.html", htmltable = cleantable)


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
