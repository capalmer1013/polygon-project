class BootStrap {

    def init = { servletContext ->

        def server = new ServerSocket(1337)

        while(true) {
            server.accept { socket ->
                println "processing new connection..."
                socket.withStreams { input, output ->
                    def reader = input.newReader()
                    def buffer = reader.readLine()
                    println "server received: $buffer"
                    def now = new Date()
                    output << "echo-response($now): " + buffer + "\n"
                }
                println "processing/thread complete."
            }
        }

    }
    def destroy = {
    }
}
