class Character(object):
    """Under the current Monaco implimentation,
    The possibilities have been exaustively created and
    no new instances of this class should be made"""
    _definitions = list()

    def __init__(self, name):
        self._name = name
        Character._definitions.append(self)
        
    def _getName(self):
        return self._name
        
    def _getXmlName(self):
        return "0" + self._name
        
    def _getDataName(self):
        name = self._getXmlName()
        name += "\x00" * (100 - len(name))
        return name 
        
def _getCharacterByDataName(name):
    for i in Character._definitions:
        if i._getDataName() == name:
            return i
    return None
        
Locksmith = Character("Locksmith")
Lookout = Character("Lookout")
Cleaner = Character("Cleaner")
Pickpocket = Character("Pickpocket")

Gentleman = Character("Gentleman")
Hacker = Character("Hacker")
Mole = Character("Mole")
Redhead = Character("Redhead")


MrPink = Character("ThiefPink")
MrPurple = Character("ThiefPurple")
MrTurquoise = Character("ThiefTurquoise")
MsOrange = Character("ThiefOrange")

CleanerPlus = Character("CleanerMole")
LocksmithPlus = Character("LocksmithHacker")
LookoutPlus = Character("LookoutRedhead")
PickpocketPlus = Character("PickpocketGentleman")