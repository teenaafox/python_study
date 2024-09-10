import socket
import threading


# class : 같은 역할을 하는 함수들의 묶음
class ChatServer:
    # __함수__ : 미리 정해져 있는 함수
    # 클래스가 호출되면 __init__함수가 먼저 실행된다. 내 정보 저장
    def __init__(self, host="localhost", port=5000):
        # self: 내 자신 안에서 관리되는 변수들
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
                # 받은 데이터를 1024바이트 크기로 디코드 해서 가공
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    break

                # 사용자 이름 변경 부분 추가
                if message.startswith("/set name "):
                    new_name = message[10:].strip()
                    if new_name:
                        old_name = self.clients[client_socket]
                        self.clients[client_socket] = new_name
                        self.broadcast(
                            f"{old_name}님이 {new_name}(으)로 이름을 변경했습니다."
                        )
                else:
                    # 서버에 붙은 클라이언트들에게 전부 broadcast
                    self.broadcast(f"{self.clients[client_socket]}: {message}")

            except ConnectionResetError:
                break

        del self.clients[client_socket]
        client_socket.close()
        self.broadcast(f"{name}님이 채팅방을 나갔습니다.")

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode("utf-8"))
            except:
                pass


if __name__ == "__main__":
    server = ChatServer()   # 함수 실행하듯 클래스도 호출
    server.start()