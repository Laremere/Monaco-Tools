
class GameMode(object):
    """Under the current Monaco implimentation,
    The possibilities have been exaustively created and
    no new instances of this class should be made"""
    _definitions = list()

    def __init__(self, value):
        self._value = value
        GameMode._definitions.append(self)
        
    def _getValue(self):
        return self._value
        
def _getGameMode(value):
    for i in GameMode._definitions:
        if i._getValue() == value:
            return i
    return None
        
        
Normal = GameMode(0)
PvP = GameMode(1)