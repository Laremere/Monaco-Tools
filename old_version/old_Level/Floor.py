import copy

#Architecture = 0
#Furniture = 1
#Item = 2
#Meta = 3

class Floor(object):
    def __init__(self):
    
        self._name = None
        self._text = [""] * 16
        self._data = [[0] * (53 * 30)] * 8
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        assert isinstance(name, str)
        self._name = name
        
    def getRoomName(self, index):
        assert 0 <= index < 16
        return self._text[index]
        
    def setRoomName(self, index, text):
        assert 0 <= index < 16
        assert isinstance(text, str)
        self._text[index] = text
        
        #There may be a requirement of this string bring null terminated
        #Not sure, if stuff breaks try it
        
    def _dumpData(self, data):
        assert len(data) == 8
        for i in data:
            assert len(i) == 53 * 30
            
        for i in data[4:]:
            for j in i:
                assert 0 <= j < 4
                
        self._data = copy.deepcopy(data)
    