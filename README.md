# FoxTurMapAndStats

This is a fan made project and is not associated with Turing Smart Screens or Siege Camp's Foxhole in any official manner. Use at your own risk.

This project utilizes the turing-smart-screen-python library and Foxhole War API to display the current world conquest war map and war information. Each screen will display for X number of seconds based on the INI configuration parameters. This project was built specifically for the 3.5" inch screen but the INI file and graphics can be modified to work with larger screens.

**Known Issues:**
        <br />
        * The LCD screen can lock up depending on the timing of the screen draw and shutdown. If the screen is drawing when the application is closing its possible the LCD will be stuck. Undocking/Unpluggin the LCD screen resolves the issue.
        <br />
        * Its possible in some cases if a computer shutdown occurs the screen will not turn off. Undocking/Unpluggin the LCD screen resolves the issue.


**Future Enhancements**
* Full integration into the Turing Smart Screen Python library.
* Foxhole 57 Update additions (Rocket Launch Sites, Rocket Devastation Location, Weather Stations)


**How to run:**
<br />
Install the required libraries (refer to requirements.txt)
<br />
Run the following script: foxTurMapAndStats.py

**This project was built and tested with the following Turing Smart Screen:**
<br />
        Revision A (Turing Smart Screen 3.5")
        
**Turing Smart Screen Python:**
<br />
https://github.com/mathoudebine/turing-smart-screen-python

**Foxhole War API:**
<br />
https://github.com/clapfoot/warapi

**Voronoi Clipping:**
<br />
https://gist.github.com/pv/8036995

**Turing Smart Screen Offical Forum:**
<br />
http://discuz.turzx.com/

**Foxhole World Map:**
![20240717_201753](https://github.com/user-attachments/assets/f463ee01-c795-4139-8b62-b788ddb046d2)

**Foxhole War Stats:**
![20240717_201804](https://github.com/user-attachments/assets/deb8308d-ba9c-4b27-b5a0-6d8d3a0d2203)

**Foxhole World Map PNG:**
![fxWorldMapMergedWithBackground](https://github.com/user-attachments/assets/03ac20c1-8cf3-42a2-9593-377cedbf9f9b)

**Foxhole War Stats PNG:**
![fxStatsBackground](https://github.com/user-attachments/assets/9308fd6c-a3e5-4bfb-8e0c-8205e5561013)

**Adjusting Shards**
<br />
In some cases multiple Foxhole wars can be running. This typically happens during major releases of the game. In this case it might be required to adjust the INI file to point to the shard you want.
<br />
In the config subfolder you can find the fxws.ini file and the following three lines.
<br />
***Shard 1:***
<br />
apiWarUrl = https://war-service-live.foxholeservices.com/api/worldconquest/war
<br />
apiWarMapsUrl = https://war-service-live.foxholeservices.com/api/worldconquest/maps/
<br />
apiWarReportURL = https://war-service-live.foxholeservices.com/api/worldconquest/warReport/
<br />
***Shard 2:***
<br />
apiWarUrl = https://war-service-live-2.foxholeservices.com/api/worldconquest/war
<br />
apiWarMapsUrl = https://war-service-live-2.foxholeservices.com/api/worldconquest/maps/
<br />
apiWarReportURL = https://war-service-live-2.foxholeservices.com/api/worldconquest/warReport/
<br />
***Shard 3:***
<br />
apiWarUrl = https://war-service-live-3.foxholeservices.com/api/worldconquest/war
<br />
apiWarMapsUrl = https://war-service-live-3.foxholeservices.com/api/worldconquest/maps/
<br />
apiWarReportURL = https://war-service-live-3.foxholeservices.com/api/worldconquest/warReport/
<br />

**FoxTurMapAndStats Specific Code Breakdwon:**
 <br />
fxwsAPI.py - Functions to call Foxhole War API.
 <br />
fxwsAPIData.py - Classes for storing Foxhole War API data.
 <br />
fxwsDataClasses.py - Classes for storing calculated runtime data.
 <br />
fxwsDrawStats.py - Main function to draw war stats image.
 <br />
fxwsFunctions.py - Functions to generate war stats data.
 <br />
fxwsLookupTables.py - Lookup table for generating war map.
 <br />
fxwsWorldMapDraw.py - Main function to draw world amp.
 <br />
fxwsWorldMapFunctions.py - Functions to help generate war map.
 <br />

