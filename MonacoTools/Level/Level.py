import StegImageReader
import LevelReader
from LevelFlags import Flags
from PIL import Image


class LevelLoadError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Level(object):
    """A monaco level"""
    def __init__(self, filePath = None, image = None, rawData = None):
        """Call  with Filepath if you want it to open and load a file
            If you already have an open PIL image, set image to it
            If you have the raw file data outside of the png, use rawData
            as an object which can be used as an iterator
            Behavior with more than one named arguement used is undefined
            If neither are entered, a blank level is created"""
            
        #Do generic Level setup
        #Level Name
        self.address = ""
        
        #Type of weather
        self.weatherName = ""
        
        #Gamemode
        #0 = Normal
        #1 = PvP
        self.gameMode = 0
        
        #Total Money
        self.totalMoney = 0
        
        #Playable Characters
        #Should only insert character objects
        self.legalCharacters = list()
        
        #Goaltype
        #0 = escape only
        #1 = collect trophies
        #2 = rescue character
        self.goalType = 0
        
        #GoalIcon
        #Path to the goal icon
        self.goalIcon = 'textures/UI/HUD/escape'
        
        #GoalText
        #Blank for escape missions
        self.goalText = ""
        
        #Respawning Money
        self.infiniteMoney = False
        
        #Dialogue
        #Should only insert Dialogue objects
        self.dialogue = list()
        
            
        if filePath == None and image == None and rawData == None:
            #Setup blank Level
            pass
            
        else:
            #Load level from file
            if filePath:
                image = Image.open(filePath)
                    
            if rawData == None:
                dataIter = StegImageReader.StegImageReader(image)
            else:
                dataIter = iter(rawData)
            
            self._load(LevelReader.LevelReader(dataIter))
     
    def _load(self, dataIter):
        floor = -1
        for key, item in dataIter:
            if key == Flags.VERSION and item != 8:
                print "Warning, map version may not be supported!"

            elif key == Flags.ADDRESS:
                self.address = item
                
            elif key == Flags.WEATHERNAME:
                self.weather = item
                
            elif key == Flags.GAMEMODE:
                self.gameMode = item
                
            elif key == Flags.TOTALMONEY:
                self.totalMoney = item
                
            elif key == Flags.LEGALCHARACTERS:
                pass
                #TODO: Impliment this
                
            elif key == Flags.GOALTYPE:
                self.goalType = item
                
            elif key == Flags.GOALICON:
                self.goalItem = item
                
            elif key == Flags.GOALTEXT:
                self.goalText = item
                
            elif key == Flags.INFINITEMONEY:
                self.infiniteMoney = item
                
            elif key == Flags.DIALOGUE:
                pass
                #todo: impliment this
                
            elif key != LevelReader.Flags.MAPDATA:
                print key, item