import pygame
from server import MySocket
from math import sin, cos, radians, pi


def point_position(x0, y0, dist, theta):
    return dist*sin(theta), dist*cos(theta)


class Character:
    # base class for character data to pass to server

    playerSpeed = 10
    playerMaxResistance = 50
    rotateCounterStart = 50

    def __init__(self, user_id, user_name, vertex_count, max_health, current_health,
                            xPos, yPos, orientation):
        spriteName = 'models/Player-Triangle-00.png'
        self.user_id = user_id
        self.user_name = user_name
        self.vertex_count = vertex_count
        self.max_health = max_health
        self.current_health = current_health
        self.xPos = xPos
        self.yPos = yPos
        self.orientation = orientation
        self.playerResistance = self.playerMaxResistance
        self.move = False
        self.rotate_right = False
        self.rotate_left = False
        self.rotateCounter = self.rotateCounterStart
        self.sprite = pygame.image.load(spriteName)
        self.sprite.set_alpha(255)
        self.playerRect = self.sprite.get_rect()
        self.rot_tuple = (self.sprite, self.playerRect)

    def serialize_class(self):
        ser = bytearray(2048)
        ser.append(0)
        ser.append(0)
        ser.append(1)
        ser.append(self.user_id)
        ser.append(self.vertex_count)
        ser.append(self.max_health)
        ser.append(self.current_health)
        ser.append(self.xPos)
        ser.append(self.yPos)
        ser.append(self.orientation)
        # ser.append(self.user_name + "\0")
        for i in self.user_name + "\0":
            ser.append(i)
        # print("first two bytes are the size of packet, inclusive")
        temp = len(ser)
        byte1 = (temp & 0b1111111100000000) >> 8
        byte2 = temp & 0b0000000011111111
        ser.insert(0, byte1)
        ser.insert(1, byte2)
        return ser

    def get_update(self):
        ser = bytearray()
        #ser_len = (ser.__getitem__(0)<<8) & ser.__getitem__(1)
        self.user_id = ser.__getitem__(3)

    def to_string(self):
        print("ID: %i" % self.user_id)
        print("USER: %s" % self.user_name)
        print("V-TEX COUNT: %i" % self.vertex_count)
        print("xPOS %i" % self.xPos)
        print("yPos %i" % self.yPos)
        print("ORIENTATION %i" % self.orientation)

    def cycle(self):
        if self.rotate_right:
            self.rotateCounter -= 1
            if self.rotateCounter == 0:
                self.orientation -= 10
                self.rotateCounter = self.rotateCounterStart

        if self.rotate_left:
            self.rotateCounter -= 1
            if self.rotateCounter == 0:
                self.orientation += 10
                self.rotateCounter = self.rotateCounterStart

        if self.move:
            xyTuple = point_position(0, 0, self.playerSpeed, radians(self.orientation))
            self.playerResistance -= 1
            if self.playerResistance == 0:
                self.playerResistance = self.playerMaxResistance
                self.xPos -= xyTuple[0]
                self.yPos -= xyTuple[1]

Brent = Character(12, "blaze_it_bitch", 3, 10, 4, 69, 69, 120)
# Brent.to_string()
mySocket = MySocket.MySocket()

mySocket.connect("10.8.62.228", 1337)
# print Brent.serialize_class()
mySocket.mysend(Brent.serialize_class())

temp_buffer = mySocket.myreceive()
print temp_buffer

