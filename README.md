# spotify-info
This program is a very simple api project that pulls data from Spotify based on a user token and outputs song information

## Things to Consider:
**PLEASE DO NOT DO ANY OF THIS IN THE FOLDER YOUR SPOTIFY IS INSTALLED IN, IT MAY OR MAY NOT BREAK YOUR OFFICIAL SPOTIFY APP OR PLEASE RENAME THE .py FILE**
- Only works for windows as of 4/8/2023 <br>
- Redirects to http://localhost:8080/callback so if you already got something there, maybe its not a bad idea to change the redirect url : ) <br>
- The application requires a valid client.txt file containing the client_id and client_secret for the Spotify API. This file should be placed in the same directory as the exe file. Follow the official [Spotify Documentation](https://developer.spotify.com/documentation/web-api/) to set it up. <br>
- When you have an appropriate client.txt file with the formatting <br>
<br> client_id=YOUR_CLIENT_ID 
<br> client_secret=YOUR_CLIENT_SECRET <br> <br>
- You can make it into an exe with your integrated client details running this command in terminal <br> <br> python3 -m PyInstaller --onefile --noconsole --add-data "client.txt;."  spotify.py  <br>
