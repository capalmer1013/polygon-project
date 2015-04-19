package polygon.server

import java.nio.Buffer

class Character {

    static constraints = {
    }

    short id;
    short vertexCount
    short maxHealth
    short currentHealth
    short xPos
    short yPos
    short orientation
    String username

    Character(Buffer bytes){
        //this = bytes.asType(Character);
    }
}