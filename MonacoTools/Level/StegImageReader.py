class StegImageReader(object):
    """Takes a PIL image and reads the pixels into  map data bytes"""
    
    def __init__(self, image):
        self.pixels = image.getdata()
        self._iterBitsObj = self._iterBits()

    def _iterBits(self):
        for digit in [1 << i for i in xrange(0,8)]:
            for pixel in self.pixels:
                for channel in xrange(1,3):
                    yield 1 if ( pixel[channel] & digit ) else 0
    
        raise StopIteration
                    
    def next(self):
        value = 0
        for i in xrange(7,-1,-1):
            value += self._iterBitsObj.next() << i
        return value