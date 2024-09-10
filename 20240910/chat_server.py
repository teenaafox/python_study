import socket
import threading


class ChatServer:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"서버가 {self.host}:{self.port}에서 시작되었습니다.")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"새로운 연결: {address}")
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_thread.start()

    def handle_client(self, client_socket):
        name = "익명"
        self.clients[client_socket] = name
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                if message.startswith("/set name"):
                    new_name = message[10:].strip()
                    if new_name:
                        old_name = self.clients[client_socket]
                        self.clients[client_socket] =new_name
                        self.broadcast(
                            f"{old_name}님이 {new_name}(으)로 이름을 변경했습니다."
                        )
                else:
                    self.broadcast(f"{self.clients[client_socket]}: {message}")

            except ConnectionResetError:
                break

        del self.clients[client_socket]
        client_socket.close()
        sef.broadcast(f"{name}님이 채팅방을 나갔습니다.")

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode("utf-8"))
            except:
                pass


if __name__ == "__main__":
    server = ChatServer()
    server.start()

            