from library.log import logger

from asyncio.log import logger
import matplotlib.pyplot as plt
from foxMapAndStats.fxwsDataClasses import *
from foxMapAndStats.fxwsLookupTables import *
from foxMapAndStats.fxwsWorldMapFunctions import *
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from shapely.geometry import Point


def fxWorldMapDraw(fxWarConquest, fxWorkingData, foxholeFont, fxConfig):

        logger.debug("Building worldmap.")

        #Store Generated Map Regions
        fxWorldMapRegions = []

        #Voronoi Bounding Hex
        fxVorBoundingHex = Polygon([[.25, 0], [.75, 0], [1, 0.49], [1, 0.51], [.75, 1], [.25, 1], [0, .51], [0, .49]])

        #Iterate through region data and generate region maps
        for fxWarMapStatic in fxWarConquest.fxWarMapStatics:

            logger.debug("Generating Region Map for Region ID: " + str(fxWarMapStatic.regionId))

            #Create Region Map Holder and lookup region map
            fxWorldMapStatic = fxRegionDrawData(fxWarMapStatic.regionId,fxRegionMapLookup[fxWarMapStatic.regionId])

            #Iterate through static region items looking for MAJOR points
            for fxWarStaticMapTextItem in fxWarMapStatic.mapTextItems:
                if (fxWarStaticMapTextItem.mapMarkerType == "Major"):
                    fxWorldMapStatic.fxSubRegionPoints.append([fxWarStaticMapTextItem.x, fxWarStaticMapTextItem.y])

            #Generate Voronoi Data
            vor = Voronoi(fxWorldMapStatic.fxSubRegionPoints)

            #Geneerate Region and Vertices Data
            logger.debug("Generating Voronoi Diagram")
            fxWorldMapStatic.fxRegionRegions, fxWorldMapStatic.fxRegionVertices = voronoi_finite_polygons_2d(vor)

            #Load Images For Drawing
            fxRegionMapRaw = Image.open(fxWorldMapStatic.fxRegionMap).convert('RGBA')  
            fxRegionMap = Image.open(fxWorldMapStatic.fxRegionMap).convert('RGBA')  
            fxDrawRegion = ImageDraw.Draw(fxRegionMap)

            #Draw and Colorize Regions
            logger.debug("Clipping Voronoi Diagram.")
            for region in fxWorldMapStatic.fxRegionRegions:
                polygon = fxWorldMapStatic.fxRegionVertices[region]
                # Clipping polygon
                poly = Polygon(polygon)
                poly = poly.intersection(fxVorBoundingHex)
                polygon = [p for p in poly.exterior.coords]
                plt.fill(*zip(*polygon), alpha=0.4)

                #Update polygon points to work with region map sizes
                updatedPoints = []
                for point in polygon:
                    updatedPoints.append(find_pixel_location(fxRegionMap.width,fxRegionMap.height,point[0] * 100,point[1] * 100))

                #Save updated points for redrawing polygons after merge
                #The merge reduces the visibility of subregion borders which requires a redraw of the lines
                fxWorldMapStatic.fxSubRegionPolygons.append(updatedPoints)

                #Determine subregion faction ownership
                logger.debug("Determining faction ownership by subregion.")
                for fxWarMapRegion in fxWarConquest.fxWarMapRegions:
                    #Find war map region data
                    if fxWarMapRegion.regionId == fxWarMapStatic.regionId:
                        #Iterate through map items
                        for fxWarMapRegionMapItem in fxWarMapRegion.mapItems:
                            #Check and see if an item is a townhall or relic
                            if (fxWarMapRegionMapItem.iconType in (45,46,47,56,57,58)):
                                #Determine pixel location of map item
                                fxPoint = Point(find_pixel_location(fxRegionMap.width, fxRegionMap.height, fxWarMapRegionMapItem.x * 100, fxWarMapRegionMapItem.y * 100))
                                #Iterate through updated points and draw once pixel location is found within an updated point
                                if(fxPoint.within(Polygon(updatedPoints)) == True):
                                    logger.debug("Setting ownership for: " + str(fxWarMapRegionMapItem.x) + "  " + str(fxWarMapRegionMapItem.y))
                                    if fxWarMapRegionMapItem.teamId == "COLONIALS":
                                        fxDrawRegion.polygon(updatedPoints, fill = fxConfig['WorldMap']['fxWorldMapColonial'], outline ="#000000")
                                    elif fxWarMapRegionMapItem.teamId == "WARDENS":
                                        fxDrawRegion.polygon(updatedPoints, fill = fxConfig['WorldMap']['fxWorldMapWarden'], outline ="#000000")
                                    elif fxWarMapRegionMapItem.teamId == "NONE":
                                        fxDrawRegion.polygon(updatedPoints, fill = fxConfig['WorldMap']['fxWorldMapNeutral'], outline ="#000000")

            #Merge Foxhole Region Map with Drawn Regions
            logger.debug("Merging region map with drawn subregions.")
            fxWorldMapRegionMerge = Image.blend(fxRegionMapRaw, fxRegionMap, 0.50)
 
            #Redraw region borders
            logger.debug("Redrawing subregion borders.")
            for fxSubRegionPolygons in fxWorldMapStatic.fxSubRegionPolygons:
                fxDrawSubRegionLines = ImageDraw.Draw(fxWorldMapRegionMerge)
                fxDrawSubRegionLines.line(fxSubRegionPolygons, fill="black", width=4)
            
            #Debug: Save Region Map
            if(fxConfig['Log']['Debug'] == 'True'):
                logger.debug("Saving region map to working directory.")
                fxWorldMapRegionMerge.save("res/working/" + str(fxWorldMapStatic.regionId) + ".png")

            #Save generated map to memory
            fxWorldMapStatic.fxRegionGeneratedMap = fxWorldMapRegionMerge
            fxWorldMapRegions.append(fxWorldMapStatic)

            logger.debug("Finished Generating Region Map for Region ID: " + str(fxWarMapStatic.regionId))

        #Generate World Maps
        worldMapHeight = 7
        worldMapWidth = 7
        rawMapWidth = 1024
        rawMapHeight = 888

        fxWorldMapCanvas = Image.new(mode="RGBA", size=(round(worldMapWidth * rawMapWidth),worldMapHeight * rawMapHeight))

        for fxWarMapRegion in fxWorldMapRegions:
            #Stitch maps together
            fxWorldMapPositions = fxRegionPositionLookup[fxWarMapRegion.regionId]
            fxWorldMapPositionX = round(fxWorldMapPositions[0] * rawMapWidth)
            fxWorldMapPositionY = round(fxWorldMapPositions[1] * rawMapHeight)

            fxWorldMapCanvas.paste(fxWarMapRegion.fxRegionGeneratedMap, (fxWorldMapPositionX, fxWorldMapPositionY), fxWarMapRegion.fxRegionGeneratedMap)

        #Debug: Save World Canvas
        if(fxConfig['Log']['Debug'] == 'True'):
            logger.debug("Saving world map to working directory.")
            fxWorldMapCanvas.save("res/working/worldmap.png")

        #Resize World Map to fit on background
        fxWorldMapCanvas = fxWorldMapCanvas.resize(eval(fxConfig['WorldMap']['fxWorldMapCanvasSize']),Image.LANCZOS)

        #Debug: Save World Canvas Resized
        if(fxConfig['Log']['Debug'] == 'True'):
            logger.debug("Saving world map resized to working directory.")
            fxWorldMapCanvas.save("res/working/worldmap-resized.png")

        #Merge All Elements
        fxWorldMapBackground = Image.open(fxConfig['WorldMap']['fxWorldMapBackground']).convert('RGBA')
        fxVictoryPointFlagColonial = Image.open(fxConfig['WorldMap']['fxWorldMapVictoryPointFlagColonial']).convert('RGBA')
        fxVictoryPointFlagWarden = Image.open(fxConfig['WorldMap']['fxWorldMapVictoryPointFlagWarden']).convert('RGBA')

        #Paste World Map onto Background
        fxWorldMapBackground.paste(fxWorldMapCanvas, eval(fxConfig['WorldMap']['fxWorldMapCanvasXY']), fxWorldMapCanvas)
        #Paste Colonial VP Icon onto Background
        fxWorldMapBackground.paste(fxVictoryPointFlagColonial, eval(fxConfig['WorldMap']['fxWorldMapVictoryPointFlagColonialXY']), fxVictoryPointFlagColonial)
        #Paste Warden VP Icon onto Background
        fxWorldMapBackground.paste(fxVictoryPointFlagWarden, eval(fxConfig['WorldMap']['fxWorldMapVictoryPointFlagWardenXY']), fxVictoryPointFlagWarden)

        #Add Victory Point Text
        fxFoxholeFont = ImageFont.truetype(foxholeFont, eval(fxConfig['WorldMap']['fxWorldMapFontSize']))
        colonialVictoryPoints = str(fxWorkingData.fxTotalColonialVictoryPoints) + "/" + str(fxWarConquest.fxWarData.requiredVictoryTowns)
        wardenVictoryPoints = str(fxWorkingData.fxTotalWardenVictoryPoints) + "/" + str(fxWarConquest.fxWarData.requiredVictoryTowns)

        fxDrawText = ImageDraw.Draw(fxWorldMapBackground)

        fxDrawText.text(eval(fxConfig['WorldMap']['fxWorldMapColonialVictoryPoints']), colonialVictoryPoints, anchor="ms", fill ="black", font = fxFoxholeFont, align ="center") 
        fxDrawText.text(eval(fxConfig['WorldMap']['fxWorldMapWardenVictoryPoints']), wardenVictoryPoints, anchor="ms", fill ="black", font = fxFoxholeFont, align ="center")
        
        #Draw Warden Rocket Information
        fxWardenRocketSite = Image.open(fxConfig['WorldMap']['fxWorldMapRocketSiteWarden']).convert('RGBA')
        fxWardenRocketSiteArmed = Image.open(fxConfig['WorldMap']['fxWorldMapRocketSiteArmedWarden']).convert('RGBA')
        
        #Warden Rocket Site
        fxWorldMapBackground.paste(fxWardenRocketSite, eval(fxConfig['WorldMap']['fxWarMapWardenRocketSiteXY']), fxWardenRocketSite)
        #Warden Armed Rocket Site
        fxWorldMapBackground.paste(fxWardenRocketSiteArmed, eval(fxConfig['WorldMap']['fxWarMapWardenRocketSiteArmedXY']), fxWardenRocketSiteArmed)
        #Warden Rocket Sites Count
        fxDrawText = ImageDraw.Draw(fxWorldMapBackground)    
        fxDrawText.text(eval(fxConfig['WorldMap']['fxWarMapTotalWardenRocketSitesXY']), str(fxWorkingData.fxTotalWardenRocketSilos), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
        fxDrawText.text(eval(fxConfig['WorldMap']['fxWarMapTotalWardenRocketSitesArmedXY']), str(fxWorkingData.fxTotalWardenArmedRocketSilos), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")

        #Draw Colonial Rocket Information
        fxColonialRocketSite = Image.open(fxConfig['WorldMap']['fxWorldMapRocketSiteColonial']).convert('RGBA')
        fxColonialRocketSiteArmed = Image.open(fxConfig['WorldMap']['fxWorldMapRocketSiteArmedColonial']).convert('RGBA')

        #Colonial Rocket Site
        fxWorldMapBackground.paste(fxColonialRocketSite, eval(fxConfig['WorldMap']['fxWarMapColonialRocketSiteXY']), fxColonialRocketSite)
        #Colonial Armed Rocket Site
        fxWorldMapBackground.paste(fxColonialRocketSiteArmed, eval(fxConfig['WorldMap']['fxWarMapColonialRocketSiteArmedXY']), fxColonialRocketSiteArmed)
        #Colonial Rocket Sites Count
        fxDrawText = ImageDraw.Draw(fxWorldMapBackground)    
        fxDrawText.text(eval(fxConfig['WorldMap']['fxWarMapTotalColonialRocketSitesXY']), str(fxWorkingData.fxTotalColonialRocketSilos), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
        fxDrawText.text(eval(fxConfig['WorldMap']['fxWarMapTotalColonialRocketSitesArmedXY']), str(fxWorkingData.fxTotalColonialArmedRocketSilos), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center") 
        


        #Debug: Save Final Background
        if(fxConfig['Log']['Debug'] == 'True'):
            logger.debug("Saving final world map to working directory.")
            fxWorldMapBackground.save("res/working/fxWorldMapMergedWithBackground.png")

        logger.debug("Worldmap Complete.")

        return fxWorldMapBackground

