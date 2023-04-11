from flask import Flask, render_template

# render template objects to all be kept in specially named 'templates' folder,
# with this EXACT spelling

app = Flask("anything")


@app.route("/")  # slash for default page
def home():
    return render_template("weather.html")


@app.route("/api/v1/<station>/<date>")  #note syntax for dynamic variables
def lookup(station, date):
    print(station, date)
    return [station, date]


app.run(debug=True) #can add eg port=5001 if running multiple apps. 
