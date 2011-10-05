    class Planet(object):
    def __init__(self, x, y, radius, player):
        self.x = x
        self.y = y
        self.radius = radius
        self.player = player
        self.color = (1.0, 1.0, 1.0)


    def get_planets(min_x, min_y, max_x, max_y):
        return [Planet(1,1, 5, 1), Planet(10,12, 5,1), Planet(10, 0, 5, 2)]
