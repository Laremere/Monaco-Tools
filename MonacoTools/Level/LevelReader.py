Flags = type("MapFlags", (), {a:b for b,a in enumerate([
        "VERSION",
        "WORLDNAME",
        "ADDRESS",
        "SUBTITLE",
        "STARTTITLE",
        "WEATHERNAME",
        "TOTALMONEY",
        "LEGALCHARACTERS",
        "GOALTYPE",
        "MAPSTART",
        "MAPNAME",
        "ROOMNAMES",
        "LOOTCOUNT",
        "MAPDATA",
        "EOF",
        "GOALTEXT",
        "GOALICON",
        "INFINITEMONEY",
        "DIALOGUE",
        "GAMEMODE",
    ])})

        
class LevelReader(object):
    """Takes a PIL image and reads the pixels into  map data bytes"""
    
    def __init__(self, rawData):
        self.rawData = rawData
        
    def _nextByte(self):
        self.rawData.next()
        
    def _nextShortInt(self):
        num = self.rawData.next() 
        num += self.rawData.next() << 8
        return num
        
    def _nextLongInt(self):
        num = self.rawData.next() << 24
        num += self.rawData.next() << 16
        num += self.rawData.next() << 8
        num += self.rawData.next()
        return num
        
    def _readNumber(self):
        length = self.rawData.next()
        num = 0
        for i in range(0, length):
            num += self.rawData.next() << (i * 8)
            
    def _readString(self):
        length = self.rawData.next()
        mystr = ""
        for i in range(0, length):
            mystr += chr(self.rawData.next())
        return mystr
        
    def _readStringArray(self):
        count = self.rawData.next()
        strings = list()
        for i in range(0, count):
            strings.append(self._readString())
        
        return strings
        
    def _readMapData(self):
        run_length = self._nextLongInt()
        longindex = list()
        
        for i in xrange(0,run_length / 2):
            length = self._nextShortInt() + 1
            tile = self._nextShortInt()
            for j in range(0, length):
                longindex.append(tile)
                
        layers = list()
        for i in xrange(0,8):
            this = i * 53 * 30
            next = (i + 1) * 53 * 30
            layers.append(longindex[this:next])
            
        return layers
        
    def _readNone(self):
        return None
    
    _nextTag = [_readNone, _nextByte, _readNumber, _readString, _readStringArray, _readMapData]
        
    def next(self):
        flag = self.rawData.next()
        if flag == Flags.EOF:
            raise StopIteration
        data = self._nextTag[ self.rawData.next() ](self)
        return flag, data
        
    def __iter__(self):
        return self