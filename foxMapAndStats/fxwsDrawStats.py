from pickle import NONE
from PIL import Image, ImageDraw, ImageFont
import logging

def fxDrawStats(fxWarConquest, fxWorkingData, foxholeFont, fxConfig):

    logging.debug("Building stats image.")

    #Determine background based on victory points
    if fxWorkingData.fxTotalColonialVictoryPoints > fxWorkingData.fxTotalWardenVictoryPoints:
        fxStatsBackground = Image.open(fxConfig['Stats']['fxStatsColonialBackground']).convert('RGBA') 
    elif fxWorkingData.fxTotalWardenVictoryPoints > fxWorkingData.fxTotalColonialVictoryPoints:
        fxStatsBackground = Image.open(fxConfig['Stats']['fxStatsWardenBackground']).convert('RGBA') 
    elif fxWorkingData.fxTotalWardenVictoryPoints == fxWorkingData.fxTotalColonialVictoryPoints:
        fxStatsBackground = Image.open(fxConfig['Stats']['fxStatsTiedBackground']).convert('RGBA')

    #Open Icons
    fxIntelCenterColonial = Image.open(fxConfig['Stats']['fxStatsIntelCenterColonial']).convert('RGBA')
    fxIntelCenterWarden = Image.open(fxConfig['Stats']['fxStatsIntelCenterWarden']).convert('RGBA')
    fxStormCannonColonial = Image.open(fxConfig['Stats']['fxStatsStormCannonColonial']).convert('RGBA')
    fxStormCannonWarden = Image.open(fxConfig['Stats']['fxStatsStormCannonWarden']).convert('RGBA')
    fxStatsFactoryColonial = Image.open(fxConfig['Stats']['fxStatsFactoryColonial']).convert('RGBA')
    fxStatsFactoryWarden = Image.open(fxConfig['Stats']['fxStatsFactoryWarden']).convert('RGBA')
    fxStatsMPFColonial = Image.open(fxConfig['Stats']['fxStatsMPFColonial']).convert('RGBA')
    fxStatsMPFWarden = Image.open(fxConfig['Stats']['fxStatsMPFWarden']).convert('RGBA')
    fxStatsRefineryColonial = Image.open(fxConfig['Stats']['fxStatsRefineryColonial']).convert('RGBA')
    fxStatsRefineryWarden = Image.open(fxConfig['Stats']['fxStatsRefineryWarden']).convert('RGBA')
        
    fxStatsBackground.paste(fxIntelCenterColonial, eval(fxConfig['Stats']['fxStatsIntelCenterColonialXY']), fxIntelCenterColonial)
    fxStatsBackground.paste(fxIntelCenterWarden, eval(fxConfig['Stats']['fxStatsIntelCenterWardenXY']), fxIntelCenterWarden) 
    fxStatsBackground.paste(fxStormCannonColonial, eval(fxConfig['Stats']['fxStatsStormCannonColonialXY']), fxStormCannonColonial)    
    fxStatsBackground.paste(fxStormCannonWarden, eval(fxConfig['Stats']['fxStatsStormCannonWardenXY']), fxStormCannonWarden)
    fxStatsBackground.paste(fxStatsFactoryColonial, eval(fxConfig['Stats']['fxStatsFactoryColonialXY']), fxStatsFactoryColonial)
    fxStatsBackground.paste(fxStatsFactoryWarden, eval(fxConfig['Stats']['fxStatsFactoryWardenXY']), fxStatsFactoryWarden)
    fxStatsBackground.paste(fxStatsMPFColonial, eval(fxConfig['Stats']['fxStatsMPFColonialXY']), fxStatsMPFColonial)
    fxStatsBackground.paste(fxStatsMPFWarden, eval(fxConfig['Stats']['fxStatsMPFWardenXY']), fxStatsMPFWarden)
    fxStatsBackground.paste(fxStatsRefineryColonial, eval(fxConfig['Stats']['fxStatsRefineryColonialXY']), fxStatsRefineryColonial)
    fxStatsBackground.paste(fxStatsRefineryWarden, eval(fxConfig['Stats']['fxStatsRefineryWardenXY']), fxStatsRefineryWarden)

    #Draw Stats Text
    fxDrawText = ImageDraw.Draw(fxStatsBackground)    
    fxFoxholeFont = ImageFont.truetype(foxholeFont, eval(fxConfig['Stats']['fxStatsFontSize']))
    
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsWarNumberXY']), "War Number: " + str(fxWarConquest.fxWarData.warNumber), fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsWarDurationXY']), "War Duration: " + fxWorkingData.fxWarLength, fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsWardenCasualtiesXY']), "Warden Casualties: " + str(f"{fxWorkingData.fxTotalWardenCasualties:,}"), fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsColonialCasualtiesXY']), "Colonial Casualties: " + str(f"{fxWorkingData.fxTotalColonialCasualties:,}"), fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalWarCasualtiesXY']), "Total Casualties: " + str(f"{fxWorkingData.fxTotalWarCasualties:,}"), fill ="white", font = fxFoxholeFont, align ="center")    
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalStormCannonsWardenXY']), str(fxWorkingData.fxTotalWardenStormCannons), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalStormCannonsColonialXY']), str(fxWorkingData.fxTotalColonialStormCannons), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalIntelCentersWardenXY']), str(fxWorkingData.fxTotalWardenIntelCenters), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalIntelCentersColonialXY']), str(fxWorkingData.fxTotalColonialIntelCenters), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalMPFColonialXY']), str(fxWorkingData.fxTotalColonialMPFs), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalMPFWardenXY']), str(fxWorkingData.fxTotalWardenMPFs), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalRefineryColonialXY']), str(fxWorkingData.fxTotalColonialRefineries), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalRefineryWardenXY']), str(fxWorkingData.fxTotalWardenRefineries), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalFactoryColonialXY']), str(fxWorkingData.fxTotalColonialFactories), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")
    fxDrawText.text(eval(fxConfig['Stats']['fxStatsTotalFactoryWardenXY']), str(fxWorkingData.fxTotalWardenFactories), anchor="ms", fill ="white", font = fxFoxholeFont, align ="center")

    if(fxWorkingData.fxResistanceLength != None):
        fxDrawText.text(eval(fxConfig['Stats']['fxStatsResistanceMode']), "(Resistance Mode)", fill ="white", font = fxFoxholeFont, align ="center")

    #Debug
    if(fxConfig['Log']['Debug']):
        logging.debug("Saving final world map to working directory.")
        fxStatsBackground.save("res/working/fxStatsBackground.png")

    logging.debug("Building of stats image complete.")

    return fxStatsBackground