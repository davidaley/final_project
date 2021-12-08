# Welcome to Songmapper! 

Built by David Aley and Luke Kolar, this website allows users to connect to their Spotify accounts and create a visual representation of their listening history by keeping track of where in the world you first listened to a song or where it holds a strong memory. Using the Spotify developer API and Leaflet.js, this website first connects a user's Spotify account, then redirects to a page with a map using Leaflet.js. From there, user's can look throughout the map and click anywhere to add a song from their saved songs library. Over time, a user can populate a world map with their favorite songs and create their very own Songmap!

This website was built using Flask, HTML, Javascript, CSS, and SQL. Flask was used to build our backend database, HTML was used to build the structure of the frontend of the website, Javascript was primarily used to implement our map feature (using Leaflet.js), and we built a database using SQL to store information about our user's maps.

URL to video: https://www.youtube.com/watch?v=xCVYlQlfLwM

If you are testing this website, please use a Spotify dummy account we created as we need to authorize every Spotify user who logs in to our website:
        - Email: mciacblooalapxxhfu@nvhrw.com
        - Password: thisiscs50

## Initial Setup

Download all files in the repository, and open with Visual Studio Code (or some other coding environment). Some libraries in app.py may not be available in the base environment, so we created a virtual environment called ".venv" to install and use the necessary packages. 

To navigate into the virtual enviroment, enter "source .venv/bin/activate" and the virtual environment should show up as "(.venv) in the command line.

We built the backend using Flask, so to run our program, enter "Flask run" in the command line and then either follow the link provided or run "localhost:5000" in your browser. 

If an error comes up, it is most likely with the imports of various libraries. You may need to create a new virtual environment using the command "python3 -m venv /path/to/new/virtual/environment", and then "source /path/to/new/virtual/environment/bin/activate" to navigate to the virtual environment. From here, use the command "pip install <library name>" to ensure that the necessary libraries are imported. The necessary libraries needed to run this website are listed below in the "Requirements" section.
        
Once on the website, you will be taken to a homepage. Follow the directions to log in using your Spotify credentials (default to using the Spotify dummy account listed above unless otherwise instructed). 
        
And there you go! You should be all set up and ready to use Songmapper!
        
For any questions, technical issues, or other comments, feel free to email us at davidaley@college.harvard.edu and/or lukekolar@college.harvard.edu

## Requirements

Requirements for Songmapper are generally preinstalled in both Flask and Python3, however, for custom installs the following packages are required:

        - flask
        - flask_session
        - cs50
        - pandas
        - requests
        - json
            
## Sources

Using the Spotify API and leaflet.js were fairly tricky, and we couldn't have fixed some issues in our project and completed a product we were proud of without the help from the following sources:
        - Vibester (https://github.com/JayA96/Vibester)
        - Flask-Spotify-Auth (https://github.com/vanortg/Flask-Spotify-Auth)
        - Spotify Developer Website (https://developer.spotify.com/)
        - Leaflet.js (https://leafletjs.com/)
        - Nicepage (https://nicepage.com/)
