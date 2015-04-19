class LoginController {
    SocketService ss = new SocketService()

    def index() {
         [hello: "Hello World Bitches"]
    }
    def getSocket() {
        ss.serviceMethod();
    }
}
