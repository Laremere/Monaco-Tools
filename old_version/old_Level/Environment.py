class Environment(object):
    """Under the current Monaco implimentation,
    The possibilities have been exaustively created and
    no new instances of this class should be made"""
    _definitions = list()

    def __init__(self, identity):
        self._identity = identity
        Environment._definitions.append(self)
        
    def _getIdentity(self):
        return self._identity
        
def _getEnvironment(identity):
    for i in Environment._definitions:
        if i._getIdentity() == identity:
            return i
    return None
            

ArmoredCar = Environment("WeatherArmoredCar")
Banque = Environment("WeatherBanque")
Casino = Environment("WeatherCasino")
Cathedral = Environment("WeatherCathedral")
Credits = Environment("WeatherCredits")
DiamondExchange = Environment("WeatherDiamondExchange")
Docks = Environment("WeatherDocks")
Embassy = Environment("WeatherEmbassy")
Gallery = Environment("WeatherGallery")
Hospital = Environment("WeatherHospital")
Hotel = Environment("WeatherHotel")
Jardin = Environment("WeatherJardin")
Jimmyz = Environment("WeatherJimmyz")
Mansion = Environment("WeatherMansion")
Museum = Environment("WeatherMuseum")
Palace = Environment("WeatherPalace")
Prison = Environment("WeatherPrison")
Racetrack = Environment("WeatherRacetrack")
SafeHouse = Environment("WeatherSafeHouse")
Securitech = Environment("WeatherSecuritech")
Yacht = Environment("WeatherYacht")