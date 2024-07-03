#Class to store calculated data based on data from API
class fxWorkingData:
    def __init__(self):
        self.fxTotalWardenCasualties = 0
        self.fxTotalColonialCasualties = 0
        self.fxTotalColonialVictoryPoints = 0
        self.fxTotalWardenVictoryPoints = 0
        self.fxTotalWarCasualties = 0
        self.fxTotalNeutralVictoryPoints = 0
        self.fxTotalWardenStormCannons = 0
        self.fxTotalColonialStormCannons = 0
        self.fxTotalWardenIntelCenters = 0
        self.fxTotalColonialIntelCenters = 0
        self.fxTotalColonialFactories = 0
        self.fxTotalWardenFactories = 0
        self.fxTotalWardenMPFs = 0
        self.fxTotalColonialMPFs = 0
        self.fxTotalWardenRefineries = 0
        self.fxTotalColonialRefineries = 0
        self.fxWarLength = None
        self.fxResistanceLength = None

#Class to store region drawing data
class fxDrawingData:
    def __init__(self):
        self.fxRegionDrawingData = []

#Class to store regional drawing data
class fxRegionDrawData:
    def __init__(self, regionId, fxRegionMap):
        self.regionId = regionId
        self.fxRegionMap = fxRegionMap  
        self.fxRegionGeneratedMap = None
        self.fxSubRegionPoints = []
        self.fxSubRegionsDrawData = []
        self.fxSubRegionPolygons = []
        self.fxRegionVertices = []
        self.fxRegionRegions = []
        
#Class to store subregion drawing data
class fxSubRegionDrawData:
    def __init__(self, teamId, fxSubregionXY):
        self.teamId = teamId
        self.fxSubregionXY = fxSubregionXY

#Class to store subregion XY Data
class fxSubRegionVorCoordDrawData:
    def __init__(self, xCoord, yCoord):
        self.x = xCoord
        self.y = yCoord

#Class to store data from War Data from API
class fxWarData:
    def __init__(self):
        self.eTag = None
        self.warId = None
        self.warNumber = None
        self.winner = None
        self.conquestStartTime = None
        self.conquestEndTime = None
        self.resistanceStartTime = None
        self.requiredVictoryTowns = None
        self.fxWarMaps = fxWarMaps()
        self.fxWarReports = []
        self.fxWarMapRegions = []   

#Class to store list of War Maps from API
class fxWarMaps:
    def __init__(self):
        self.maps = []

#Class to store list of War Reports from API
class fxWarReport:
    def __init__(self, mapName):
        self.mapName = mapName
        self.eTag = None
        self.totalEnlistments = None
        self.colonialCasualties = None
        self.wardenCasualties = None
        self.dayOfWar = None
        self.version = None

#Class to store list of War Map Regions from API
class fxWarMapRegion:
    def __init__(self, mapRegionName):
        self.mapRegionName = mapRegionName
        self.eTag = None
        self.regionId = None
        self.scorchedVictoryTowns = None
        self.lastUpdated = None
        self.version = None
        self.mapItems = []

#Class to store list of War Region Map Items from API
class fxWarRegionMapItem:
    def __init__(self, teamId, iconType, x, y, flags):
        self.teamId = teamId
        self.iconType = iconType
        self.x = x
        self.y = y
        self.flags = flags