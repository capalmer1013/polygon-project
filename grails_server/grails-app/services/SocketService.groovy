class SocketService {
    def static globalSocket

    def serviceMethod() {
        if(!globalSocket)
            globalSocket = new ServerSocket(1337)

        while(true) {
            globalSocket.accept { socket ->
                socket.withStreams { input, output ->
                    def reader = input.newReader()
                    def buffer = reader.readLine()
                    println "server received: $buffer"
                    def now = new Date()
                    output << "echo-response($now): " + buffer + "\n"
                    /*byte[] psize = new byte[2];
                    //get the packet size (2 bytes)
                    reader.read(psize, 0, 2)
                    psize = (int)((psize[0] <<8) & psize[1])

                    //get opcode
                    byte[] opcode = []
                    reader.read(opcode, 2, 1)
                    reader.readLines().each {

                    }

                    //get data
                    byte[] data = []
                    int sizeWithoutHeader = psize - 3;
                    reader.read(data, 3, sizeWithoutHeader)

                    data.each {output.write(it)}

                    //process data


                    /*switch (opcode[0]){
                        case 1: //generic character data transfer
                            break
                    }*/
                }
            }
        }
    }
}
