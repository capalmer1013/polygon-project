from server import MySocket


class Character:
    # base class for character data to pass to server

    def __init__(self, user_id, user_name, vertex_count, max_health, current_health,
                            xPos, yPos, orientation):
        self.user_id = user_id
        self.user_name = user_name
        self.vertex_count = vertex_count
        self.max_health = max_health
        self.current_health = current_health
        self.xPos = xPos
        self.yPos = yPos
        self.orientation = orientation

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

    def to_string(self):
        print("ID: %i" % self.user_id)
        print("USER: %s" % self.user_name)
        print("V-TEX COUNT: %i" % self.vertex_count)
        print("xPOS %i" % self.xPos)
        print("yPos %i" % self.yPos)
        print("ORIENTATION %i" % self.orientation)

Brent = Character(12, "blaze_it_bitch", 3, 10, 4, 69, 69, 120)
# Brent.to_string()
mySocket = MySocket.MySocket()

mySocket.connect("10.8.62.228", 1337)
# print Brent.serialize_class()
mySocket.mysend(Brent.serialize_class())

temp_buffer = mySocket.myreceive()
print temp_buffer













































































'''

                              -    .|||||.
                                  |||||||||
                          -      ||||||  .
                              -  ||||||   >
                                ||||||| -/
                           --   ||||||'(
                        -       .'      \
                             .-'    | | |
                            /        \ \ \
              --        -  |      `---:.`.\
             ____________._>           \\_\\____ ,--.__
  --    ,--""           /    `-   .     |)_)    '\     '\
       /  "             |      .-'     /          \      '\
     ,/                  \           .'            '\     |
     | "   "   "          \         /                '\,  /
     |           " , =_____`-.   .-'_________________,--""
   - |  "    "    /"/'      /\>-' ( <
     \  "      ",/ /    -  ( <    |\_)
      \   ",",_/,-'        |\_)
   -- -'-;.__:-'
   '''
