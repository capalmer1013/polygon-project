class BootStrap {

    def init = { servletContext ->

        def server = new ServerSocket(1337)

        while(true) {
            server.accept { socket ->
                println "processing new connection..."
                socket.withStreams { input, output ->
                    def reader = input.newReader()
                    char[] psize = new char[2];
                    //get the packet size (2 bytes)
                    reader.read(psize, 0, 2)
                    psize = (int)((psize[0] <<8) & psize[1])

                    //get opcode
                    char[] opcode
                    reader.read(opcode, 2, 1)

                    //get data
                    char[] data
                    reader.read(data, 2, psize -3)

                    //process data


                    switch (opcode[0]){
                        case 1: //generic character data transfer
                            break
                    }
                }
                println "processing/thread complete."
            }
        }

    }
    def destroy = {
    }
}
