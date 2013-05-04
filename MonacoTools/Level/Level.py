import StegImageReader
import LevelReader
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
        for key, item in dataIter:
            if key != LevelReader.Flags.MAPDATA:
                print key, item