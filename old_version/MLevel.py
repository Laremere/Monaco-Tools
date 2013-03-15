import sys
from PIL import Image
import math

class MonacoFloor:
    def __init__(self):
        self.name = ""
        self.rooms = list()
        for i in range(0,16):
            self.rooms.append("\x00")
        self.data = list()
        for i in range(0,8):
            self.data.append( list())
            for j in range(0,30 * 53):
                self.data[i].append(0)

class MonacoLevel:
    def __init__(self):
        #StartTitle and Subtitle is unused so we won't store it
    
        
        #A level identifier?
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
        #Note the strings are weird and are always
        #100 characters long, with nuls after the end
        #Of the string
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
        #May be broken in current version
        # character|stage|text
        #actually is stage|character|text
        # where 0 makes it print at the top fo the screen
        # 1 makes it print at the bottom
        # (for stage)
        self.dialogue = list()
        
        #Floor data
        self.floors = list()
        for i in range(0, 8):
            self.floors.append(MonacoFloor())

    def get_xml(self):
        tag = lambda x, y: "  <" + x + ">" + y + "</" + x + ">\n"
        xml = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml += '<WorldData>\n'
        xml += tag("Version","8")
        xml += tag("GoalType",str(self.goalType))
        xml += tag("GmaeMode",str(self.gameMode))
        xml += tag("Address",self.address)
        xml += tag("GoalText",self.goalText)
        xml += tag("GoalIcon",str(self.goalIcon))
        xml += tag("Discription","")
        xml += tag("WeatherName",self.weatherName)
        xml += "<LCharacters>\n"
        for i in self.legalCharacters:
            xml+= tag("string",i.replace("\x00",""))
        xml += "</LCharacters>\n"
        xml += tag("StageIndex","0")
        xml += tag("UnlockWorld","0")
        xml += tag("UnlockStage","0")
        xml += "</WorldData>"
        return xml
        
    def load(self, reader):
        curFloor = -1
        for i in reader.data:
            if i[0] == "ADDRESS":
                self.address = i[1]
            elif i[0] == "WEATHERNAME":
                self.weatherName = i[1]
            elif i[0] == "GAMEMODE":
                self.gameMode = i[1]
            elif i[0] == "TOTALMONEY":
                self.totalMoney = i[1]
            elif i[0] == "LEGALCHARACTERS":
                self.legalCharacters = i[1]
            elif i[0] == "GOALTYPE":
                self.goalType = i[1]
            elif i[0] == "GOALICON":
                self.goalIcon = i[1]
            elif i[0] == "GOALTEXT":
                self.goalText = i[1]
            elif i[0] == "INFINITEMONEY":
                self.infiniteMoney = i[1]
            elif i[0] == "DIALOGUE":
                self.dialogue = i[1]
            elif i[0] == "MAPSTART":
                curFloor += 1
            elif curFloor >= 0:
                if i[0] == "MAPNAME":
                    self.floors[curFloor].name = i[1]
                elif i[0] == "ROOMNAMES":
                    self.floors[curFloor].rooms = i[1]
                elif i[0] == "MAPDATA":
                    self.floors[curFloor].data = i[1]
                    
    def binary(self):
        writer = LevelWriter()
        
        writer.number("VERSION",8)
        writer.string("ADDRESS", self.address)
        writer.string("WEATHERNAME", self.weatherName)
        writer.number("TOTALMONEY", self.totalMoney)
        writer.string_array("LEGALCHARACTERS", self.legalCharacters)
        writer.byte("GAMEMODE",self.gameMode)
        writer.byte("GOALTYPE",self.goalType)
        writer.string("GOALTEXT", self.goalText)
        writer.string("GOALICON", self.goalIcon)
        if self.infiniteMoney:
            writer.byte("INFINITEMONEY",1)
        writer.string_array("DIALOGUE", self.dialogue)
        
        for i in self.floors:
            writer.void("MAPSTART")
            writer.string("MAPNAME",i.name)
            writer.string_array("ROOMNAMES",i.rooms)
            writer.map_data("MAPDATA",i.data)
            
        writer.void("EOF")
        return writer.data
            
        

class StegImageReader:
    def __init__(self, _image):
        self.image = _image
        self.pixels = self.image.getdata()
        self.cur_pixel = 0
        self.cur_channel = 1
        self.cur_digit = 0
        
    def next_bit(self):
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
        
    def next_byte(self):
        value = 0
        value += self.next_bit() << 7 
        value += self.next_bit() << 6
        value += self.next_bit() << 5
        value += self.next_bit() << 4
        value += self.next_bit() << 3
        value += self.next_bit() << 2
        value += self.next_bit() << 1
        value += self.next_bit()
        return value

class LevelReader:
    def __init__(self, source_image):
        self.feed = StegImageReader(source_image)
        self.data = self.read()
        
    tags = [ \
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
        
    def next(self):
        return self.feed.next_byte()
        
    def next_short_int(self):
        num = self.next() #<< 8
        num += self.next() << 8
        return num
        
    def next_long_int(self):
        num = self.next() << 24
        num += self.next() << 16
        num += self.next() << 8
        num += self.next()
        return num
 
    def read(self):
        eof = False
        map_data = list()
        while (not eof):
            tag = self.next()
            tag_name = self.tags[tag]
            if tag_name == "EOF":
                eof = True
            else:
                method = self.next()
                if method == 0: #Empty Tag
                    tag_data = None
                elif method == 1: #Byte
                    tag_data = self.next()
                elif method == 2: #Number
                    tag_data = self.read_number()
                elif method == 3: #String
                    tag_data = self.read_string()
                elif method == 4: #String Array
                    tag_data = self.read_string_array()
                elif method == 5: #Map Data
                    tag_data = self.read_map_data()
                else:
                    print "Unkown method, returning"
                    print map_data
                    return
                map_data.append((tag_name, tag_data))
        return map_data
        
    def read_number(self):
        length = self.next()
        num = 0
        for i in range(0,length):
            num += self.next() << (i * 8)
            
        return num
        
    def read_string(self):
        length = self.next()
        mystr = ""
        for i in range(0, length):
            mystr += chr(self.next())
        return mystr

        
    def read_string_array(self):
        count = self.next()
        strings = list()
        for i in range(0, count):
            length = self.next()
            mystr = ""
            for i in range(0, length):
                mystr += chr(self.next())
            strings.append(mystr)
            
        return strings
        
    def read_map_data(self):
        run_length = self.next_long_int()
        longindex = list()
        
        for i in range(0,run_length / 2):
            length = self.next_short_int() + 1
            tile = self.next_short_int()
            for j in range(0, length):
                longindex.append(tile)
                
        layers = list()
        for i in range(0,8):
            this = i * 53 * 30
            next = (i + 1) * 53 * 30
            layers.append(longindex[this:next])
            
        return layers
        
class StegImageWriter:
    def __init__(self, image, data):
        self.image = image
        self.data = data
        
        self.curbit = 7
        self.curbyte = 0
        
        pixel_array = list()
        while (self.curbyte < len(data)):
            bit1 = self.next_bit()
            bit2 = self.next_bit()
            pixel_array.append((0, bit1 * 255, bit2 * 255))
            
        image.putdata(pixel_array)

        
    def next_bit(self):
        bit = ( self.data[self.curbyte] & pow(2,self.curbit) ) >> self.curbit
        self.curbit -= 1
        if self.curbit < 0:
            self.curbit = 7
            self.curbyte += 1
        return bit
        
        
class LevelWriter:
    def __init__(self):
        self.data = list()
        
    def tag(self, tag):
        num = 0
        while (tag is not LevelReader.tags[num]):
            num += 1
        self.data.append(num)
        
    def void(self, tag):
        self.tag(tag)
        self.data.append(0)
        
    def byte(self, tag, byte):
        self.tag(tag)
        self.data.append(1)
        self.data.append(byte)
        
    def number(self, tag, number):
        self.tag(tag)
        self.data.append(2)
        if number != 0:
            bytes = int( math.ceil( math.log(number, 256)))
        else:
            bytes = 1
        self.data.append(bytes)
        for i in range(0,bytes):
            self.data.append(number & 255)
            number = number >> 8
        
    def string(self, tag, mystr):
        self.tag(tag)
        self.data.append(3)
        self.data.append(len(mystr))
        for i in mystr:
            self.data.append(ord(i))
          
    def string_array(self, tag, array):
        self.tag(tag)
        self.data.append(4)
        self.data.append(len(array))
        for i in array:
            self.data.append(len(i))
            for j in i:
                self.data.append(ord(j))
                
    def map_data(self, tag, layers):
        self.tag(tag)
        self.data.append(5)
        
        bytes = list()
        totalShorts = 0
        
        for i in layers:
            index = 0
            while (index < len(i)):
                curRun = 0
                curTile = i[index]
                index += 1
                while(curRun < 255 and index < len(i) and curTile == i[index]):
                    curRun += 1
                    index += 1
                totalShorts += 2
                bytes.append(curRun)
                bytes.append(0)
                bytes.append(curTile & 255)
                bytes.append((curTile >> 8) & 255)
        
        self.data.append((totalShorts >> (8 * 3) & 255))
        self.data.append((totalShorts >> (8 * 2) & 255))
        self.data.append((totalShorts >> (8 * 1) & 255))
        self.data.append((totalShorts & 255))
        for i in bytes:
            self.data.append(i)
                
        
        
# def save():
    # global level
    # global im
    # global binary
    # im = Image.new("RGB", (1060,480))
    # binary = level.binary()
    # StegImageWriter(im, binary)
    # im.save("Campaign_Part2_Demo/C2M01_Prison.png")
    
    # f = open("Campaign_Part2_Demo/Story/C2M01_Prison.xml", "w")
    # f.write(level.get_xml())
    # f.close()       
def save(myLevel):
    myIm = Image.new("RGB", (1060,480))
    myBinary = myLevel.binary()
    StegImageWriter(myIm, myBinary)
    myIm.save("Campaign_Part2_Demo/C2M01_Prison.png")
    
    f = open("Campaign_Part2_Demo/Story/C2M01_Prison.xml", "w")
    f.write(myLevel.get_xml())
    f.close()
        
if __name__=="__main__":
    pass
    filepath = sys.argv[1]
    filename = filepath.split("\\")[-1][:-4]
    print filename
    
    im = Image.open(filepath)
    reader = LevelReader(im)
    level = MonacoLevel()
    level.load(reader)
    
    # f = open("out.xml", "w")
    # f.write(level.get_xml())
    # f.close()
    
    #im = Image.new("RGB", (1060,480))
    # binary = level.binary()
    # StegImageWriter(im, binary)
    # im.save("C2M01_Prison.png")
    
    