import StegImageWriter
import StegImageReader
import Environment
import Characters
import GameMode
import GoalType

class Level(object):
    """Monaco Level Object"""
    def __init__(self, filepath = None):
        self._environment = Environment.ArmoredCar
        
        self._Characters = list()
        
        self._gameMode = GameMode.Normal
        
        self._goalText = ""

        self._goalType = GoalType.Escape
        
        self._address = None
        self._totalMoney = None
        self._goalIcon = None
        self._infiniteMoney = None
        self._dialogue = None
        self._floors = None

        
        if filepath:
            self._load(filepath)
        
        if len(self._Characters) == 0:
            self._Characters = [Characters.Locksmith, \
                Characters.Lookout, \
                Characters.Pickpocket, \
                Characters.Cleaner, \
                Characters.Mole, \
                Characters.Gentleman, \
                Characters.Hacker, \
                Characters.Redhead]

    def getEnvironment(self):
        return self._environment
        
    def setEnvironment(self, env):
        assert isinstance(env, Environment.Environment)
        self._environment = env
        
    def getCharacters(self):
        return self._Characters[:]
        
    def addCharacter(self, char):
        assert isinstance(char, Characters.Character)
        if char not in self._Characters:
            self._Characters.append(char)
            
    def removeCharacter(self, char):
        assert isinstance(char, Characters.Character)
        self._Characters.remove(char)
        
    def getGameMode(self):
        return self._gameMode
        
    def setGameMode(self, gameMode):
        assert isinstance(gameMode, GameMode.GameMode)
        self._gameMode = gameMode
        
    def getGoalText(self):
        return self._goalText
    
    def setGoalText(self, text):
        assert isinstance(text, str)
        self._goalText = text
        
    def getGoalType(self):
        return self._goalType
        
    def setGoalType(self, goalType):
        assert isinstance(goalType, GoalType.GoalType)
        self._goalType = goalType


    def _load(self, filepath):
        dataPoints = StegImageReader.load(filepath)
        
        curFloor = -1
        
        for i in dataPoints:
            if i[0] == "ADDRESS":
                pass
            elif i[0] == "WEATHERNAME":
                self.setEnvironment(Environment._getEnvironment(i[1]))
            elif i[0] == "GAMEMODE":
                self.setGameMode(GameMode._getGameMode(i[1]))
            elif i[0] == "TOTALMONEY":
                pass
            elif i[0] == "LEGALCHARACTERS":
                for j in i[1]:
                    self.addCharacter(Characters._getCharacterByDataName(j))
            elif i[0] == "GOALTYPE":
                self.setGoalType(GoalType._getGoalType(i[1]))
            elif i[0] == "GOALICON":
                pass
            elif i[0] == "GOALTEXT":
                self.setGoalText(i[1])
            elif i[0] == "INFINITEMONEY":
                pass
            elif i[0] == "DIALOGUE":
                pass
            elif i[0] == "MAPSTART":
                curFloor += 1
            elif curFloor >= 0:
                if i[0] == "MAPNAME":
                    pass
                elif i[0] == "ROOMNAMES":
                    pass
                elif i[0] == "MAPDATA":
                    pass

if __name__ == "__main__":
    a = Level("C1M01_Prison.png")