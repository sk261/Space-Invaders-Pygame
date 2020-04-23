PLANET_SIZE = 100

class Game:
    def __init__(self):
        self.player = Ship()
        self.player.y = -(self.PLANET_SIZE + 10)
    
    def triggerInput(self, keys):
        if 'up' in keys:
            continue
        elif 'down' in keys:
            continue
        if 'right' in keys:
            continue
        elif 'left' in keys:
            continue
        if 'r' in keys:
            continue
        elif 'space' in keys:
            continue
        if 'q' in keys:
            continue
        elif 'e' in keys:
            continue
    

def getBackgroundImage(x, y, PLANET_SIZE)