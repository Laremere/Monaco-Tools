class GoalType(object):
    """Under the current Monaco implimentation,
    The possibilities have been exaustively created and
    no new instances of this class should be made"""
    _definitions = list()
    
    def __init__(self, value):
        self._value = value
        GoalType._definitions.append(self)
        
    def _getValue(self):
        return self._value

def _getGoalType(value):
    for i in GoalType._definitions:
        if i._getValue() == value:
            return i
    return None
        
Escape = GoalType(0)
Heist = GoalType(1)
Rescue = GoalType(2)