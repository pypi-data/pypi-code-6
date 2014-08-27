
class Rect3:
    def __init__(self, x, y, z, width, height, depth):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

    def __str__(self):
        return str("Rect3(%s,%s,%s,%s,%s,%s)" % (
            self.x, self.y, self.z, self.width, self.height, self.depth))

    def __eq__(self, obj):
        return (self.x == obj.x and self.y == obj.y and self.z == obj.z and
                self.width == obj.width and self.height == obj.height and
                self.depth == obj.depth)

    def __repr__(self):
        return str("Rect3(%s,%s,%s,%s,%s,%s)" % (
            self.x, self.y, self.z, self.width, self.height, self.depth))

    def union(self, rect):
        origin = min(self.x, rect.x), min(self.y, rect.y), min(self.z, rect.z)
        return Rect3(
            origin[0], origin[1],
            max(self.x+self.width, rect.x+rect.width) - origin[0],
            max(self.y+self.height, rect.y+rect.height) - origin[1],
            max(self.z+self.depth, rect.z+rect.depth) - origin[2])

    def contains_point(self, x, y, z):
        if (x >= self.x and x <= self.x + self.width and
                y >= self.y and y <= self.y + self.height and
                z >= self.z and z <= self.z + self.depth):
            return True
        else:
            return False

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def set_depth(self, d):
        self.depth = d

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def set_pos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    set_offset = set_pos

    def center(self):
        return (self.x + self.width / 2, self.y + self.height/2,
                self.z + self.depth/2)

#    def topleft(self):
#        return (self.x, self.y)
#
#    def topright(self):
#        return (self.x+self.width, self.y)
#
#    def bottomleft(self):
#        return (self.x, self.y+self.height)
#
#    def bottomright(self):
#        return (self.x+self.width, self.y + self.height)
#
    def colliderect(self, r2):
        return (((self.x >= r2.x and self.x < r2.x + r2.width) or
                 (r2.x >= self.x and r2.x < self.x + self.width)) and
                ((self.y >= r2.y and self.y < r2.y + r2.height) or
                 (r2.y >= self.y and r2.y < self.y + self.height)) and
                ((self.z >= r2.z and self.z < r2.z + r2.depth) or
                 (r2.z >= self.z and r2.z < self.z + self.depth)))

    def collidepoint(self, p1):
        x, y, z = p1[0], p1[1], p1[2]
        return (x >= self.x and x < self.x + self.width and
                y >= self.y and y < self.y + self.height and
                z >= self.z and z < self.z + self.depth)
