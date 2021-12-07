from flask import Flask, redirect, request, render_template, session, url_for, abort
from flask_session import Session
import requests
from helpers import get_liked_tracks, get_user_id
import startup
import pandas as pd
from cs50 import SQL

# Configure application (credit: Finance PSET)
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Allow program to use SQL database in songmap.db
db = SQL("sqlite:///songmap.db")

# Pre-home page - before user logs in
@app.route("/", methods=["GET", "POST"])
def index():

    # When Spotify Login button clicked ...
    if request.method == "POST":

        # Create empty session variables so /callback/ can run
        session["latest_song"] = "Just logged on."
        session["latest_coords"] = "Just logged on."
        session["latest_info"] = "Just logged on."

        # Redirect to logged in page (leads with /callback/)
        response = startup.getUser()
        return redirect(response)
    
    # Until Spotify Login button clicked, render pre-home page
    else:       
        return render_template("index.html")

# Home page, where SongMap is viewable
@app.route("/callback/", methods=["GET", "POST"])
def map():

    # For the Spotify API
    auth_token = request.args['code']
    startup.getUserToken(auth_token)

    # Refresh the user access token and id, store these as session variables
    session["user_spot_access"] = startup.getAccessToken()[0]
    session["user_id"] = get_user_id(session["user_spot_access"])


    # Once the "Choose Song" button is clicked, redirect to /pin
    if request.method == "POST":
        return redirect("/pin")
    
    # Otherwise, render the home page with all previous points loaded from SQL
    else:       

        # Create database of map points using SQL query
        mappoints = db.execute("SELECT * FROM mappoints WHERE user_id = ?", session["user_id"])

        # Check if map points exist for user
        if len(mappoints) == 0:

            # If not, generate the example map point and render map; use these starting points
            mappoints = db.execute("SELECT * FROM mappoints WHERE user_id = ?", "example_user_id")
            startlat = mappoints[0]["latlng"].split(",", 1)[0].split("(")[1]
            startlng = mappoints[0]["latlng"].split(", ")[1].replace(")", "")

            return render_template("map.html", mappoints=mappoints, startlat=startlat, startlng=startlng)

        # Otherwise render map with points; use starting points of first point
        else:
            startlat = mappoints[0]["latlng"].split(",", 1)[0].split("(")[1]
            startlng = mappoints[0]["latlng"].split(", ")[1].replace(")", "")
            return render_template("map.html", mappoints=mappoints, startlat=startlat, startlng=startlng)


# Submit form for mapping a song
@app.route("/pin", methods=["GET", "POST"])
def pin():

    # Takes the coordinates selected on the homepage, stores them as session variable for input into SQL 
    session["latest_coords"] = request.form.get("lat-lng")
    
    # Searches for liked songs so dropdown menu has items
    liked_songs = get_liked_tracks(session["user_spot_access"])
    n_songs = range(len(liked_songs))

    # Reset request method (this solved several issues)
    request.method = "GET"

    # Once the "Choose Song" button is clicked, redirect to intermediate /song-submit page
    if request.method == "POST":
        return redirect("/song-submit")
    
    # Otherwise, render the submit page
    else:
        return render_template("pin.html", liked_songs=liked_songs, n_songs=n_songs)

# Intermediate route between /pin and home (the user won't see these functions at work)
@app.route("/song-submit", methods=["GET", "POST"])
def submit():

    # Takes the song selected from /pin, stores it as session variable for input into SQL
    latest_song = request.form.get("song_title")
    session["latest_song"] = latest_song

    # Re-creates liked_songs data frame (in case user has liked a new song)...
    access_token = startup.getAccessToken()[0]
    liked_songs = get_liked_tracks(access_token)
    # ...creates session variable with info for "latest_song" (artist and artwork) via search
    session["latest_info"] = liked_songs.loc[liked_songs['title'] == session["latest_song"]]

    # Insert new song information (title, artist, artwork_url) and coordinates into songmap.db
    db.execute("INSERT INTO mappoints (user_id, latlng, title, artist, artwork_url) VALUES(?, ?, ?, ?, ?)", 
                   session["user_id"], session["latest_coords"], 
                   session["latest_song"], session["latest_info"].iloc[0, 1], 
                   session["latest_info"].iloc[0, 2])

    # Redirects to home page
    response = startup.getUser()
    return redirect(response)
