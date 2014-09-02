
class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return str("Rect(%s,%s,%s,%s)" % (
            self.x, self.y, self.width, self.height))

    def __eq__(self, obj):
        return (self.x == obj.x and self.y == obj.y and self.width == obj.width
                and self.height == obj.height)

    def __repr__(self):
        return str("Rect(%s,%s,%s,%s)" % (
            self.x, self.y, self.width, self.height))

    def union(self, rect):
        origin = min(self.x, rect.x), min(self.y, rect.y)
        return Rect(
            origin[0], origin[1],
            max(self.x+self.width, rect.x+rect.width) - origin[0],
            max(self.y+self.height, rect.y+rect.height) - origin[1])

    def contains_point(self, x, y):
        if (x >= self.x and x <= self.x + self.width and
                y >= self.y and y <= self.y + self.height):
            return True
        else:
            return False

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    set_offset = set_pos

    def center(self):
        return (self.x + self.width / 2, self.y + self.height/2)

    def topleft(self):
        return (self.x, self.y)

    def topright(self):
        return (self.x+self.width, self.y)

    def bottomleft(self):
        return (self.x, self.y+self.height)

    def bottomright(self):
        return (self.x+self.width, self.y + self.height)

    def colliderect(self, r2):
        return (((self.x >= r2.x and self.x < r2.x + r2.width) or
                 (r2.x >= self.x and r2.x < self.x + self.width)) and
                ((self.y >= r2.y and self.y < r2.y + r2.height) or
                 (r2.y >= self.y and r2.y < self.y + self.height)))

    def collidepoint(self, p1):
        x, y = p1[0], p1[1]
        return (x >= self.x and x < self.x + self.width and
                y >= self.y and y < self.y + self.height)
