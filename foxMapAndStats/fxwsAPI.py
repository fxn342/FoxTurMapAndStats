from foxMapAndStats.fxwsAPIData import *
import logging

#eTag Function - Performs a check on header if eTag is out of date
#Returns false when no update is required, returns true when update needed
def fxCheckeTag(fxSession, apiURL, eTag):
    #If no eTag is present, perform update
    if eTag == None:
        return True
    else:
        #If Etag does exist check if data has gone stale
        fxRegionAPIData_response = fxSession.get(apiURL, headers={'If-None-Match': eTag}) 
        if fxRegionAPIData_response.status_code == 304:
            return False
        else:
            return True

#API Function to call down War Data
def fxWarDataAPI(fxSession, apiWarUrl, fxWarConquestData):
    logging.debug("Pulling War Data.")
    #Request Data
    fxWarDataAPI_response = fxSession.get(apiWarUrl)
    fxWarDataAPISet = fxWarDataAPI_response.json()
    #Save Data Set
    fxWarConquestData.fxWarData.warId = fxWarDataAPISet["warId"]
    fxWarConquestData.fxWarData.warNumber = fxWarDataAPISet["warNumber"]
    fxWarConquestData.fxWarData.winner = fxWarDataAPISet["winner"]
    fxWarConquestData.fxWarData.conquestStartTime = fxWarDataAPISet["conquestStartTime"]
    fxWarConquestData.fxWarData.conquestEndTime = fxWarDataAPISet["conquestEndTime"]
    fxWarConquestData.fxWarData.resistanceStartTime = fxWarDataAPISet["resistanceStartTime"]
    fxWarConquestData.fxWarData.requiredVictoryTowns = fxWarDataAPISet["requiredVictoryTowns"]

#API Function to call down War Map List
def fxWarMapListDataAPI(fxSession, apiWarMapsUrl, fxWarConquestData):
    logging.debug("Pulling Map List.")
    #Request Data
    fxWarMapAPIData_response = fxSession.get(apiWarMapsUrl)
    #Save Data Set
    fxWarConquestData.fxWarMaps.maps = fxWarMapAPIData_response.json()

#API Function to call down War Report Data
def fxWarReportDataAPI(fxSession, apiWarMapsUrl, mapName, fxWarConquest): 
    #Check if war report exists, if not create the war report
    if(any(x.mapName == mapName for x in fxWarConquest.fxWarReports) == False):
        logging.debug("Creating War Report for: " + mapName)
        fxWarConquest.fxWarReports.append(fxWarReport(mapName))

    #Find the War Report
    for warReport in fxWarConquest.fxWarReports:
        if warReport.mapName == mapName:
            #Check eTag for update
            if(fxCheckeTag(fxSession, apiWarMapsUrl, warReport.eTag)):
                logging.debug("War Report Updating for: " + mapName)
                fxWarReportDataAPI_response = fxSession.get(apiWarMapsUrl)
                #Save Data Set
                fxWarReportDataSet = fxWarReportDataAPI_response.json()
                warReport.eTag = fxWarReportDataAPI_response.headers["ETag"]
                warReport.totalEnlistments = fxWarReportDataSet["totalEnlistments"]
                warReport.colonialCasualties = fxWarReportDataSet["colonialCasualties"]
                warReport.wardenCasualties = fxWarReportDataSet["wardenCasualties"]
                warReport.dayOfWar = fxWarReportDataSet["dayOfWar"]
                warReport.version = fxWarReportDataSet["version"]

                #API doesn't provide reigon ID for war reports. Here we link the mapname to the static war map data mapname and pull over region ID.
                #This allows for using either mapName or regionID to link data and keeps object consistency
                for fxWarMapStatic in fxWarConquest.fxWarMapStatics:
                    if fxWarMapStatic.mapName == warReport.mapName:
                        warReport.regionId = fxWarMapStatic.regionId
                        break
            else:
                logging.debug("War Report Current: " + mapName)

#API Function to call down War Map (Regional) Data
def fxWarMapRegionDataAPI(fxSession, apiWarMapsUrl, mapName, fxWarConquest):
    #Check if war region exists, if not create the war region
    if(any(_fxWarMapRegion.mapName == mapName for _fxWarMapRegion in fxWarConquest.fxWarMapRegions) == False):
        logging.debug("Creating War Map Region for: " + mapName)
        fxWarConquest.fxWarMapRegions.append(fxWarMapRegion(mapName))

    #Find the War Map Region
    for _fxWarMapRegion in fxWarConquest.fxWarMapRegions:
        if _fxWarMapRegion.mapName == mapName:
            #Check eTag for update
            if(fxCheckeTag(fxSession, apiWarMapsUrl, _fxWarMapRegion.eTag)):
                logging.debug("War Map Region Updating for: " + mapName)
                fxWarMapRegionDataAPI_response = fxSession.get(apiWarMapsUrl)
                #Save Data Set
                fxWarMapRegionDataSet = fxWarMapRegionDataAPI_response.json()
                _fxWarMapRegion.eTag = fxWarMapRegionDataAPI_response.headers["ETag"]
                _fxWarMapRegion.regionId = fxWarMapRegionDataSet["regionId"]
                _fxWarMapRegion.scorchedVictoryTowns = fxWarMapRegionDataSet["scorchedVictoryTowns"]
                _fxWarMapRegion.lastUpdated = fxWarMapRegionDataSet["lastUpdated"]
                _fxWarMapRegion.version = fxWarMapRegionDataSet["version"]
                
                #Clear Current Map Items
                _fxWarMapRegion.mapItems.clear()

                #Iterate through Map Items
                mapItems = fxWarMapRegionDataSet["mapItems"]
                for mapItem in mapItems:
                    _fxWarMapRegion.mapItems.append(fxWarMapItem(mapItem["teamId"], mapItem["iconType"], mapItem["x"], mapItem["y"], mapItem["flags"]))
            else:
                logging.debug("War Map Region Current: " + mapName)

#API Function to call down War Map Static Data
def fxWarMapStaticDataAPI(fxSession, apiWarMapsUrl, mapName, fxWarConquest):
    #Create object to store war map static data
    _fxWarMapStatic = fxWarMapStatic(mapName)
    logging.debug("Pulling static data for: " + mapName)
    fxWarMapStaticDataAPI_response = fxSession.get(apiWarMapsUrl)
    fxWarMapStaticDataSet = fxWarMapStaticDataAPI_response.json()

    #Assign Data
    _fxWarMapStatic.mapName = mapName
    _fxWarMapStatic.regionId = fxWarMapStaticDataSet["regionId"]
    _fxWarMapStatic.scorchedVictoryTowns = fxWarMapStaticDataSet["scorchedVictoryTowns"]
    _fxWarMapStatic.lastUpdated = fxWarMapStaticDataSet["lastUpdated"]
    _fxWarMapStatic.version = fxWarMapStaticDataSet["version"]

    #Iterate through Map Text Items
    fxWarMapStaticMapItems = fxWarMapStaticDataSet["mapTextItems"]
    for _fxWarMapStaticMapItem in fxWarMapStaticMapItems:
        _fxWarMapStatic.mapTextItems.append(fxWarMapStaticMapItem(_fxWarMapStaticMapItem["text"], _fxWarMapStaticMapItem["x"], _fxWarMapStaticMapItem["y"], _fxWarMapStaticMapItem["mapMarkerType"]))

    fxWarConquest.fxWarMapStatics.append(_fxWarMapStatic)