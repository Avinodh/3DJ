# 3DJ - A browser based gesture controlled music remixer that uses the MYO gesture bracelet, LEAP motion sensor and Spotify's Echo Nest API to let user's remix music in their browsers. 

- TOP 10 BEST APPS AT PENN APPS 2015 
- SPOTIFY API PRIZE WINNER

An Oculus Rift was also used in our demo to provide a real-time visualization of the music.

Project overview: http://challengepost.com/software/3dj
Penn Apps Top 10 presentation: http://www.youtube.com/watch?v=5Mt8Bbb3p80&t=12m50s
_______________________________________________________________________________

Set Up: 
- Install the Myo and LEAP SDKs
- Make sure your MYO and LEAP motion sensor are connected to your system
- Place the required MYO (and other required) header files in the same directory as myo.cpp and compile and run myo.cpp
- Place the required LEAP (and other required) included files in the same directory as LEAP.py and run LEAP.py
- At this point, the program corresponding to myo.cpp should be reading motion data from the MYO bracelet and transmitting this data in real-time to control.php on the web server
- The LEAP.py program will simulate different key-presses depending on the hand gesture it senses
- Make sure you have a Database with a table set up with names corresponding to the one defined in the php scripts
- Load the webpage (home.php)
- The MYO will be used to control the volume of the music playing in the browser (Raise your hand up to increase the volume, lower it to decrease the volume)
- The LEAP motion sensor will be used to add effects to the music using various hand gestures
_______________________________________________________________________________

Working:
- myo.cpp receives numeric data corresponding to the bracelet's current position and transmits this numeric data in real-time via HTTP requests to control.php, from where it is subsequently stored in an SQL database
- Everytime a new session is started, myo.cpp sends a request to cleardb.php to reset the database so as to flush out all old values from previous sessions
- Data from the MYO is stored into the database at 20 values/second
- The webpage home.php once loaded begins to fetch the MYO bracelet data from the database in real-time using fetch.js
- fetch.js continously fetches the most recent value in the database(corresponding to the most recent gesture). 
- If the numeric value received is higher than the music's equilibrium volume value, the volume is increased based on the numeric value received. If the numeric value received is lower, the volume is decreased
- If no MYO is connected, the music will default to 0 volume
- The inline javascript in home.php controls the volume and effects of the music. The script compares the simulated key-press from LEAP.py to pre-defined characters, and changes the music based on the key-press simulated in the system by the LEAP.py program
- remix.js initializes the various functions needed to remix the music, and makes use of Spotify's Echo Nest API
- cleardb.php resets the database at the beginning of every session
- control.php stores the values from the MYO into the SQL database

