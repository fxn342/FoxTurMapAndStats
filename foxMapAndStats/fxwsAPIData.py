#Class to store data from Conquest War Data
class fxWarConquestData:
    def __init__(self):
        self.fxWarData = fxWarData()
        self.fxWarMaps = fxWarMaps()
        self.fxWarReports = []
        self.fxWarMapRegions = []
        self.fxWarMapStatics = []

#Class to store list of War Maps from API
class fxWarMaps:
    def __init__(self):
        self.maps = []

#Class to store data from War Data from API
class fxWarData:
    def __init__(self):
        self.warId = None
        self.warNumber = None
        self.winner = None
        self.conquestStartTime = None
        self.conquestEndTime = None
        self.resistanceStartTime = None
        self.requiredVictoryTowns = None

#Class to store static war data
class fxWarMapStatic:
    def __init__(self, mapName):
        self.mapName = mapName
        self.regionId = None
        self.eTag = None
        self.scorchedVictoryTowns = None
        self.lastUpdated = None
        self.version = None
        self.mapTextItems = []

#Class to store list of War Reports from API
class fxWarReport:
    def __init__(self, mapName):
        self.mapName = mapName
        self.regionId = None
        self.eTag = None
        self.totalEnlistments = None
        self.colonialCasualties = None
        self.wardenCasualties = None
        self.dayOfWar = None
        self.version = None
  
#Class to store list of War Map Regions from API
class fxWarMapRegion:
    def __init__(self, mapName):
        self.mapName = mapName
        self.regionId = None
        self.eTag = None      
        self.scorchedVictoryTowns = None
        self.lastUpdated = None
        self.version = None
        self.mapItems = []

#Class to store list of War Region Map Items from API
class fxWarMapItem:
    def __init__(self, teamId, iconType, x, y, flags):
        self.teamId = teamId
        self.iconType = iconType
        self.x = x
        self.y = y
        self.flags = flags

#Class to store list of War Static Map Items from API
class fxWarMapStaticMapItem:
    def __init__(self, text, x, y, mapMarkerType):
        self.text = text
        self.x = x
        self.y = y    
        self.mapMarkerType = mapMarkerType