#!/usr/bin/env python
# turing-smart-screen-python - a Python system monitor and library for USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/

# Copyright (C) 2021-2023  Matthieu Houdebine (mathoudebine)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file is a simple Python test program using the library code to display custom content on screen (see README)

import os
import signal
import sys
import time
import configparser
import traceback
import requests
from datetime import datetime

# Import only the modules for LCD communication
from library.lcd.lcd_comm_rev_a import LcdCommRevA, Orientation
from library.lcd.lcd_comm_rev_b import LcdCommRevB
from library.lcd.lcd_comm_rev_c import LcdCommRevC
from library.lcd.lcd_comm_rev_d import LcdCommRevD
from library.lcd.lcd_simulated import LcdSimulated
from library.log import logger

#FoxMapAndStats Modules
from requests.adapters import HTTPAdapter, Retry
from foxMapAndStats.fxwsAPI import *
from foxMapAndStats.fxwsDataClasses import *
from foxMapAndStats.fxwsFunctions import *
from foxMapAndStats.fxwsDrawStats import *
from foxMapAndStats.fxwsWorldMapDraw import*

# Set your COM port e.g. COM3 for Windows, /dev/ttyACM0 for Linux, etc. or "AUTO" for auto-discovery
# COM_PORT = "/dev/ttyACM0"
# COM_PORT = "COM5"
COM_PORT = "AUTO"

# Display revision:
# - A      for Turing 3.5" and UsbPCMonitor 3.5"/5"
# - B      for Xuanfang 3.5" (inc. flagship)
# - C      for Turing 5"
# - D      for Kipye Qiye Smart Display 3.5"
# - SIMU   for 3.5" simulated LCD (image written in screencap.png)
# - SIMU5  for 5" simulated LCD
# To identify your smart screen: https://github.com/mathoudebine/turing-smart-screen-python/wiki/Hardware-revisions
REVISION = "A"

stop = False

if __name__ == "__main__":
    logger.setLevel(logging.INFO) 
    fxConfig = configparser.ConfigParser()

    try:
        print("Importing FoxTurPy INI File.")
        fxConfig.read('res/config/foxturpy.ini')
        fxConfig.sections()
    except Exception as e:
        logger.error("Configuration File Error")
        logger.error(e)
        wait = input("Press Enter to continue.")
        exit(1)

    logger.setLevel(logging.INFO)
    
    def sighandler(signum, frame):
        global stop
        stop = True

    # Set the signal handlers, to send a complete frame to the LCD before exit
    signal.signal(signal.SIGINT, sighandler)
    signal.signal(signal.SIGTERM, sighandler)
    is_posix = os.name == 'posix'
    if is_posix:
        signal.signal(signal.SIGQUIT, sighandler)

    # Build your LcdComm object based on the HW revision
    lcd_comm = None
    if REVISION == "A":
        logger.info("Selected Hardware Revision A (Turing Smart Screen 3.5\" & UsbPCMonitor 3.5\"/5\")")
        # NOTE: If you have UsbPCMonitor 5" you need to change the width/height to 480x800 below
        lcd_comm = LcdCommRevA(com_port=COM_PORT, display_width=320, display_height=480)
    elif REVISION == "B":
        logger.info("Selected Hardware Revision B (XuanFang screen 3.5\" version B / flagship)")
        lcd_comm = LcdCommRevB(com_port=COM_PORT)
    elif REVISION == "C":
        logger.info("Selected Hardware Revision C (Turing Smart Screen 5\")")
        lcd_comm = LcdCommRevC(com_port=COM_PORT)
    elif REVISION == "D":
        logger.info("Selected Hardware Revision D (Kipye Qiye Smart Display 3.5\")")
        lcd_comm = LcdCommRevD(com_port=COM_PORT)
    elif REVISION == "SIMU":
        logger.info("Selected 3.5\" Simulated LCD")
        lcd_comm = LcdSimulated(display_width=320, display_height=480)
    elif REVISION == "SIMU5":
        logger.info("Selected 5\" Simulated LCD")
        lcd_comm = LcdSimulated(display_width=480, display_height=800)
    else:
        logger.error("Unknown revision")
        try:
            sys.exit(1)
        except:
            os._exit(1)

    # Reset screen in case it was in an unstable state (screen is also cleared)
    lcd_comm.Reset()

    # Send initialization commands
    lcd_comm.InitializeComm()

    # Set brightness in % (warning: revision A display can get hot at high brightness! Keep value at 50% max for rev. A)
    lcd_comm.SetBrightness(level=10)

    # Set backplate RGB LED color (for supported HW only)
    lcd_comm.SetBackplateLedColor(led_color=(255, 255, 255))

    # Set orientation (screen starts in Portrait)
    lcd_comm.SetOrientation(orientation=Orientation.LANDSCAPE)
    
    #Foxhole API URLS
    fxAPIWarUrl = fxConfig['URLS']['apiWarUrl']
    fxAPIWarMapsUrl = fxConfig['URLS']['apiWarMapsUrl']
    fxAPIWarReportURL = fxConfig['URLS']['apiWarReportURL']
    
    #Foxhole Font
    foxholeFont = fxConfig['Fonts']['foxholeFont']

    #Create War Data Object
    fxWarConquest = fxWarConquestData()
    logger.info("Start main loop.")
    
    while not stop:
        try:
            #Create session object
            fxSession = requests.Session()
            fxRetries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
            fxSession.mount('http://', HTTPAdapter(max_retries=fxRetries))
            
            #Pull war List        
            fxWarDataAPI(fxSession, fxAPIWarUrl, fxWarConquest)
            
            #Only pull map list once
            if len(fxWarConquest.fxWarMaps.maps) == 0:
                fxWarMapListDataAPI(fxSession, fxAPIWarMapsUrl, fxWarConquest)
                
            #Only pull map statics once
            if len(fxWarConquest.fxWarMapStatics) == 0:
                for mapName in fxWarConquest.fxWarMaps.maps:
                    fxWarMapStaticDataAPI(fxSession, (fxAPIWarMapsUrl + mapName + "/static"), mapName, fxWarConquest)
            
            #Pull casualty and region data
            for mapName in fxWarConquest.fxWarMaps.maps:
                fxWarReportDataAPI(fxSession, (fxAPIWarReportURL + mapName), mapName, fxWarConquest)
                fxWarMapRegionDataAPI(fxSession, (fxAPIWarMapsUrl + mapName + "/dynamic/public"), mapName, fxWarConquest)
                
            #Close session
            fxSession.close()
            
            #Reset working data object
            _fxWorkingData = fxWorkingData()
            
            #Generate Working Data
            _fxWorkingData = fxPopulateWorkingData(fxWarConquest)
            
            #Display Victory Screen (if winner is declared)
            if fxConfig['Display']['fxDisplayVictoryScreen'] == "True":
                if fxWarConquest.fxWarData.winner != "NONE":
                    logger.info("Displaying victory background.")
                    if fxWarConquest.fxWarData.winner == "COLONIALS":
                        lcd_comm.DisplayPILImage(Image.open(fxConfig['Victory']['fxColonialVictoryScreen']).convert('RGBA'))
                        time.sleep(int(fxConfig['Timers']['fxDisplayVictoryFor']))
                    if fxWarConquest.fxWarData.winner == "WARDENS":
                        lcd_comm.DisplayPILImage(Image.open(fxConfig['Victory']['fxWardenVictoryScreen']).convert('RGBA'))
                        time.sleep(int(fxConfig['Timers']['fxDisplayVictoryFor']))

            #Generate world map background
            if fxConfig['Display']['fxDisplayWorldMap'] == "True":
                logger.info("Generating world map.")
                lcd_comm.DisplayPILImage(fxWorldMapDraw(fxWarConquest, _fxWorkingData, foxholeFont,fxConfig))
                logger.info("Displaying world map.")
                time.sleep(int(fxConfig['Timers']['fxDisplayWorldMapFor']))

            #Generate stats background
            if fxConfig['Display']['fxDisplayStatsScreen'] == "True":
                logger.info("Generating stats.")
                lcd_comm.DisplayPILImage(fxDrawStats(fxWarConquest, _fxWorkingData, foxholeFont,fxConfig))
                logger.info("Displaying stats.")
                time.sleep(int(fxConfig['Timers']['fxDisplayStatsFor']))

            #Fail safe to prevent runaway calls
            if fxConfig['Display']['fxDisplayVictoryScreen'] != "True" and fxConfig['Display']['fxDisplayWorldMap'] != "True" and fxConfig['Display']['fxDisplayStatsScreen'] != "True":
                logger.info("Fail safe detected. Check config file display settings.")
                time.sleep(int(fxConfig['Timers']['fxFailSafeDelay']))
            
        except Exception as e:
            logger.critical("Error in Main Loop")
            logging.error(traceback.format_exc())
            time.sleep(int(fxConfig['Timers']['fxExceptionRetryDelay']))
            #Clear War Data
            fxWarConquest = fxWarConquestData()

    # Close serial connection at exit
    lcd_comm.closeSerial()
