# FoxTurMapAndStats

This is a fan made project and is not associated with Turing Smart Screens or Siege Camp's Foxhole in any official manner. Use at your own risk.

This project utilizes the turing-smart-screen-python library and Foxhole War API to display the current world conquest war map and war information. Each screen will display for X number of seconds based on the INI configuration parameters. This project was built specifically for the 3.5" inch screen but the INI file and graphics can be modified to work with larger screens.

**Known Issues:**
        <br />
        The LCD screen can lock up depending on the timing of the screen draw and shutdown. If the screen is drawing when the application is closing its possible the LCD will be stuck. Undocking/Unpluggin the LCD screen resolves the issue.
        <br />
        <br />
        Its possible in some cases if a computer shutdown occurs the screen will not turn off. Undocking/Unpluggin the LCD screen resolves the issue.

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
![screen01](https://github.com/fxn342/FoxTurMapAndStats/assets/141661840/0439cc06-40df-4111-8cd8-1ca2d950da22)

**Foxhole War Stats:**
![screen02](https://github.com/fxn342/FoxTurMapAndStats/assets/141661840/9dcd2317-c1f4-437f-8f5f-f2d27627634d)


FoxTurMapAndStats Specific Code Breakdwon:
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

