from hashlib import md5

class Planet(object):
    def __init__(self, x, y, radius, player):
        self.x = x
        self.y = y
        self.radius = radius
        self.player = player
        self.color = (1.0, 1.0, 1.0)



def get_planets(min_x, min_y, max_x, max_y):
    start_x = min_x - min_x % 30
    start_y = min_y - min_y % 30
    re = []
    for x in xrange(start_x, max_x, 30):
        for y in xrange(start_y, max_y, 30):
            m = md5('%i:%i' % (x, y)).digest()
            for planet in xrange(8):
                add_x = int(ord(m[planet*2]) / 256. * 30)
                add_y = int(ord(m[planet*2+1]) / 256. * 30)
                re.append(Planet(x + add_x, y + add_y, 10, 0))
    return re

