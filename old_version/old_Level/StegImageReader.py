import Image

        
class __StegImageReader(object):
    def __init__(self, filepath):
        image = Image.open(filepath)
        self.pixels = image.getdata()
        self.cur_pixel = 0
        self.cur_channel = 1
        self.cur_digit = 0

    def _nextBit(self):
        pixel = self.pixels[self.cur_pixel]
        channel = pixel[self.cur_channel]
        value = channel & (1 << self.cur_digit)
        
        if value:
            value = 1
        
        self.cur_channel += 1
        if self.cur_channel >= 3:
            self.cur_channel = 1
            self.cur_pixel += 1
        if self.cur_pixel >= len(self.pixels):
            self.cur_digit += 1
            self.cur_pixel = 0
            
        return value
        
    def _nextByte(self):
        value = 0
        value += self._nextBit() << 7 
        value += self._nextBit() << 6
        value += self._nextBit() << 5
        value += self._nextBit() << 4
        value += self._nextBit() << 3
        value += self._nextBit() << 2
        value += self._nextBit() << 1
        value += self._nextBit()
        return value
        
    def _nextShortInt(self):
        num = self._nextByte() #<< 8
        num += self._nextByte() << 8
        return num
        
    def _nextLongInt(self):
        num = self._nextByte() << 24
        num += self._nextByte() << 16
        num += self._nextByte() << 8
        num += self._nextByte()
        return num
        
    def _readNumber(self):
        length = self._nextByte()
        num = 0
        for i in range(0, length):
            num += self._nextByte() << (i * 8)
            
    def _readString(self):
        length = self._nextByte()
        mystr = ""
        for i in range(0, length):
            mystr += chr(self._nextByte())
        return mystr
        
    def _readStringArray(self):
        count = self._nextByte()
        strings = list()
        for i in range(0, count):
            strings.append(self._readString())
        
        return strings
        
    def _readMapData(self):
        run_length = self._nextLongInt()
        longindex = list()
        
        for i in range(0,run_length / 2):
            length = self._nextShortInt() + 1
            tile = self._nextShortInt()
            for j in range(0, length):
                longindex.append(tile)
                
        layers = list()
        for i in range(0,8):
            this = i * 53 * 30
            next = (i + 1) * 53 * 30
            layers.append(longindex[this:next])
            
        return layers
        
    def _readNone(self):
        return None
    
    _tags = [ \
            "VERSION", \
            "WORLDNAME", \
            "ADDRESS", \
            "SUBTITLE", \
            "STARTTITLE", \
            "WEATHERNAME", \
            "TOTALMONEY", \
            "LEGALCHARACTERS", \
            "GOALTYPE", \
            "MAPSTART", \
            "MAPNAME", \
            "ROOMNAMES", \
            "LOOTCOUNT", \
            "MAPDATA", \
            "EOF", \
            "GOALTEXT", \
            "GOALICON", \
            "INFINITEMONEY", \
            "DIALOGUE", \
            "GAMEMODE", \
            ]
        
    _nextTag = [_readNone, _nextByte, _readNumber, _readString, _readStringArray, _readMapData]
    
    def next(self):
        tag = self._tags[self._nextByte()]
        if tag == "EOF":
            return ("EOF", None)
        data = self._nextTag[self._nextByte()](self)
        return (tag, data)
        
        
def load(filepath):
    reader = __StegImageReader(filepath)
    EOF = False
    dataPoints = list()
    while not EOF:
        dataPoints.append(reader.next())
        #print dataPoints[-1][0]
        if dataPoints[-1][0] == "EOF":
            EOF = True
            
    return dataPoints
    
if __name__ == "__main__":
    level = load("C1M01_Prison.png")