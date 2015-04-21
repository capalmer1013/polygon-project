import pygame
import random
from server import MySocket
from math import sin, cos, radians, pi

white = 255, 255, 255

def point_position(x0, y0, dist, theta):
    return dist*sin(theta), dist*cos(theta)

shapeDict = {3: 'triangle',
             4: 'square',
             5: 'pentagon',
             6: 'hexagon',
             7: 'heptagon',
             8: 'octagon',
             9: 'nonagon',
             10: 'decagon',
             0: 'circle'}


class Character:
    # base class for character data to pass to server

    playerSpeed = 1
    playerMaxResistance = 1
    rotateCounterStart = 1

    def __init__(self, user_id, user_name, vertex_count, max_health, current_health,
                            xPos, yPos, orientation):

        self.attackPower = vertex_count * 20
        self.attackCount = self.attackPower
        self.attack = False
        self.wall = False
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
        self.spriteName = 'models/Player-'+shapeDict[vertex_count]+'-'+str(self.roundHealth(current_health))+'.png'
        self.sprite = pygame.image.load(self.spriteName)
        self.sprite.set_colorkey(white)
        self.sprite.set_alpha(255)
        self.Rect = self.sprite.get_rect()
        self.rect = self.sprite.get_rect()
        self.rot_tuple = (self.sprite, self.Rect)

    def roundHealth(self, health):
        returnHealth = 0
        if health > 0:
            returnHealth = 25
        if health > 25:
            returnHealth = 50
        if health > 50:
            returnHealth = 75
        if health > 75:
            returnHealth = 100
        return returnHealth

    def updateHealth(self):
        self.spriteName = 'models/Player-'+shapeDict[vertex_count]+'-'+str(self.roundHealth(self.current_health))+'.png'
        self.sprite = pygame.image.load(self.spriteName)

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
        # ser_len = (ser.__getitem__(0)<<8) & ser.__getitem__(1)
        self.user_id = ser.__getitem__(3)
        self.vertex_count = ser.__getitem__(4)
        self.max_health = ser.__getitem__(5)
        self.current_health = ser.__getitem__(6)
        self.xPos = ser.__getitem__(7)
        self.yPos = ser.__getitem__(8)
        self.orientation = ser.__getitem__(9)

        flag = True
        i = 10
        while flag:
            user_name_byte = ser.__getitem__(i)
            if user_name_byte == "\0":
                flag = False
            else:
                self.user_name += user_name_byte

    def to_string(self):
        print("ID: %i" % self.user_id)
        print("USER: %s" % self.user_name)
        print("V-TEX COUNT: %i" % self.vertex_count)
        print("xPOS %i" % self.xPos)
        print("yPos %i" % self.yPos)
        print("ORIENTATION %i" % self.orientation)

    def moveBack(self, speed):
        xyTuple = point_position(0, 0, speed*2, radians((self.orientation+180) % 360))
        self.playerResistance -= 1
        if self.playerResistance == 0:
            self.playerResistance = self.playerMaxResistance
            self.xPos -= xyTuple[0]
            self.yPos -= xyTuple[1]

    def cycle(self):
        if self.attack:
            if self.attackCount > 0:
                self.orientation -= 10
                self.attackCount -= 1
            else:
                self.attackCount = self.vertex_count * self.attackPower
                self.attack = False

        if self.rotate_right:
            self.rotateCounter -= 1
            if self.rotateCounter == 0:
                self.orientation -= 1
                self.rotateCounter = self.rotateCounterStart

        if self.rotate_left:
            self.rotateCounter -= 1
            if self.rotateCounter == 0:
                self.orientation += 1
                self.rotateCounter = self.rotateCounterStart

        if self.move:
            xyTuple = point_position(0, 0, self.playerSpeed, radians(self.orientation))
            self.playerResistance -= 1
            if self.playerResistance == 0:
                self.playerResistance = self.playerMaxResistance
                self.xPos -= xyTuple[0]
                self.yPos -= xyTuple[1]
        self.rect = self.sprite.get_rect()


class npc():
    playerSpeed = 1
    user_id = -1
    user_name = 'npc'
    max_health = 100

    def __init__(self, vertex_count, xPos, yPos, orientation):
        self.dieTimer = 30
        self.attack = False
        self.wall = False
        self.vertex_count = vertex_count
        self.xPos = xPos
        self.yPos = yPos
        self.orientation = orientation
        self.current_health = 100
        self.spriteName = 'models/Player-'+shapeDict[self.vertex_count]+'-'+str(self.current_health)+'.png'
        self.sprite = pygame.image.load(self.spriteName)
        self.sprite.set_colorkey(white)
        self.sprite.set_alpha(255)
        self.Rect = self.sprite.get_rect()
        self.rect = self.sprite.get_rect()
        self.rot_tuple = (self.sprite, self.Rect)
        self.attack = False
        self.rotate_right = False
        self.rotate_left = False
        self.move = False

    def roundHealth(self, health):
        returnHealth = 0
        if health > 0:
            returnHealth = 25
        if health > 25:
            returnHealth = 50
        if health > 50:
            returnHealth = 75
        if health > 75:
            returnHealth = 100
        return returnHealth

    def updateHealth(self):
        self.spriteName = 'models/Player-'+shapeDict[self.vertex_count]+'-'+str(self.roundHealth(self.current_health))+'.png'
        self.sprite = pygame.image.load(self.spriteName)
        print self.current_health


    def moveBack(self, speed):
        xyTuple = point_position(0, 0, speed*2, radians((self.orientation+180) % 360))
        self.xPos -= xyTuple[0]
        self.yPos -= xyTuple[1]

    def cycle(self):
        chance = random.randint(3, 10)
        if self.wall:
            self.rotate_left = True
            self.move = False
            self.wall = False
        else:
            if chance < 15:
                chance2 = random.randint(1, 5)
                if chance2 == 1:
                    self.rotate_right = False
                    self.rotate_left = True
                elif chance2 == 2:
                    self.rotate_left = False
                    self.rotate_right = True
                else:
                    self.move = True
            else:
                self.move = False
        if self.current_health == 0:
            self.move = False
            self.rotate_left = False
            self.rotate_right = False

        if self.rotate_right:
            self.orientation -= 1

        if self.rotate_left:
            self.orientation += 1

        if self.move:
            xyTuple = point_position(0, 0, self.playerSpeed, radians(self.orientation))
            self.xPos -= xyTuple[0]
            self.yPos -= xyTuple[1]
        self.rect = self.sprite.get_rect()



Brent = Character(12, "BrentosorousRex", 3, 10, 25, 69, 69, 120)
Brent.to_string()
mySocket = MySocket.MySocket()

mySocket.connect("54.149.175.19", 1337)
# print Brent.serialize_class()
mySocket.mysend(Brent.serialize_class())

temp_buffer = mySocket.myreceive()
print temp_buffer



