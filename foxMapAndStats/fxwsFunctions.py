import logging
from foxMapAndStats.fxwsDataClasses import *
import datetime
import time

#Populate Working Data
def fxPopulateWorkingData(fxWarConquest):

    #Create new Working Data Object
    _fxWorkingData = fxWorkingData()

    wardens = "WARDENS"
    colonials = "COLONIALS"
    neutral = "NONE"

    #Calculate Total Casualties per side
    logging.debug("Calculating casualty counts per faction.")
    for fxWarReport in fxWarConquest.fxWarReports:
        _fxWorkingData.fxTotalWardenCasualties += fxWarReport.wardenCasualties
        _fxWorkingData.fxTotalColonialCasualties += fxWarReport.colonialCasualties

    #Calculate Total War casualties
    logging.debug("Calculating total war casualties.")
    _fxWorkingData.fxTotalWarCasualties = _fxWorkingData.fxTotalWardenCasualties + _fxWorkingData.fxTotalColonialCasualties

    #Calculate Ownership totals
    logging.debug("Calculating ownership totals per faction.")
    for fxWarMapRegion in fxWarConquest.fxWarMapRegions:
        for fxWarRegionMapItem in fxWarMapRegion.mapItems:
            if fxWarRegionMapItem.iconType == 59:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenStormCannons += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialStormCannons += 1
            if fxWarRegionMapItem.iconType == 60:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenIntelCenters += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialIntelCenters += 1
            if fxWarRegionMapItem.iconType == 17:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenRefineries += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialRefineries += 1
            if fxWarRegionMapItem.iconType == 34:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenFactories += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialFactories += 1
            if fxWarRegionMapItem.iconType == 51:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenMPFs += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialMPFs += 1
            if fxWarRegionMapItem.iconType == 37:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenRocketSilos += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialRocketSilos += 1
            if fxWarRegionMapItem.iconType == 72:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenArmedRocketSilos += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialArmedRocketSilos += 1
            if fxWarRegionMapItem.iconType == 888:
                if fxWarRegionMapItem.teamId == wardens:
                    _fxWorkingData.fxTotalWardenWeatherStations += 1
                if fxWarRegionMapItem.teamId == colonials:
                    _fxWorkingData.fxTotalColonialWeatherStations += 1

    #Calculate Victory Points
    logging.debug("Calculating total victory points per faction.")
    for fxWarMapRegion in fxWarConquest.fxWarMapRegions:
        for fxWarRegionMapItem in fxWarMapRegion.mapItems:
            if (fxWarRegionMapItem.iconType == 45 or 
                fxWarRegionMapItem.iconType == 46 or 
                fxWarRegionMapItem.iconType == 47 or 
                fxWarRegionMapItem.iconType == 56 or 
                fxWarRegionMapItem.iconType == 57 or 
                fxWarRegionMapItem.iconType == 58):
                        # First column is true, second column is false
                        #                                          T,F
                        #IsVictoryBase           (0x01) - Position 9,8
                        #IsHomeBase              (0x02) - Position 7,6
                        #IsBuildSite             (0x04) - Position 5,4
                        #IsScorched              (0x10) - Position 3,2
                        #IsTownClaimed           (0x20) - Position 1,0
                    flags = (bin(fxWarRegionMapItem.flags)[2:].zfill(10))
                    if (flags[9] == "1"):
                        if(fxWarRegionMapItem.teamId == wardens):
                            _fxWorkingData.fxTotalWardenVictoryPoints += 1
                        if(fxWarRegionMapItem.teamId == colonials):
                            _fxWorkingData.fxTotalColonialVictoryPoints += 1
                        if(fxWarRegionMapItem.teamId == neutral):
                            _fxWorkingData.fxTotalNeutralVictoryPoints += 1

    #Calculate War Length
    #Potential Bug: Resistance length (time) was off by five hours compared to foxholestats
    #Potential Rework: Update these time calculations into single function.
    logging.debug("Calculating war length.")
    if(fxWarConquest.fxWarData.conquestEndTime == None):
        startTime = fxWarConquest.fxWarData.conquestStartTime
        converted_startTime = datetime.datetime.fromtimestamp(round(startTime / 1000))
        current_time_utc = datetime.datetime.utcnow()
        warLength = current_time_utc - converted_startTime
        hours = time.strftime('%H', time.gmtime(warLength.seconds))
        minutes = time.strftime('%M', time.gmtime(warLength.seconds))
        _fxWorkingData.fxWarLength = (str(warLength.days) + " days " + str(hours) + " hours and " + str(minutes) + " minutes")
    else:
        startTime = fxWarConquest.fxWarData.conquestStartTime
        endTime = fxWarConquest.fxWarData.conquestEndTime
        converted_startTime = datetime.datetime.fromtimestamp(round(startTime / 1000))
        converted_endTime = datetime.datetime.fromtimestamp(round(endTime / 1000))
        warLength = converted_endTime - converted_startTime
        hours = time.strftime('%H', time.gmtime(warLength.seconds))
        minutes = time.strftime('%M', time.gmtime(warLength.seconds))
        _fxWorkingData.fxWarLength = (str(warLength.days) + " days " + str(hours) + " hours and " + str(minutes) + " minutes")

    #Calculate Resistance Length
    logging.debug("Calculating resistance length.")
    if(fxWarConquest.fxWarData.resistanceStartTime != None):
        startTime = fxWarConquest.fxWarData.resistanceStartTime
        converted_startTime = datetime.datetime.fromtimestamp(round(startTime / 1000))
        current_time_utc = datetime.datetime.utcnow()
        warLength = current_time_utc - converted_startTime
        hours = time.strftime('%H', time.gmtime(warLength.seconds))
        minutes = time.strftime('%M', time.gmtime(warLength.seconds))
        _fxWorkingData.fxResistanceLength = (str(warLength.days) + " days " + str(hours) + " hours and " + str(minutes) + " minutes")
    return _fxWorkingData
