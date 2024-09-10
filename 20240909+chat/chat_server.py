import socket
import threading

# 이 서버는 여러 클라이언트의 연결을 받아 메시지를 주고받으며, 클라이언트는 자신의 이름을 설정할 수 있다.

# ChatServer라는 클래스를 정의하여 서버의 동작을 관리
class ChatServer:
	# 클래스의 생성자 메서드. 서버가 실행될 때 필요한 초기 설정
	# host="localhost": 서버가 로컬에서 실행됨을 의미
	# port=5000: 서버가 5000번 포트에서 통신을 리스닝
	def __init__(self, host="localhost", port=5000):
		# 생성자에서 받은 host와 port 값을 클래스의 인스턴스 변수로 저장
		self.host = host 
		self.port = port 
		# 서버 소켓을 생성
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 현재 연결된 클라이언트 소켓과 그들의 이름을 저장할 딕셔너리
		self.clients = {}

	# 서버를 시작하는 메서드
	def start(self):
		# 서버 소켓을 host와 port에 바인딩하여, 이 주소에서 연결 요청을 받을 준비
		self.server_socket.bind((self.host, self.port))
		# 서버 소켓이 연결을 대기(listen)
		self.server_socket.listen()
		print(f"서버가 {self.host}:{self.port}에서 시작되었습니다.")

		while True:
			# 클라이언트가 서버에 연결을 시도하면, 
			# accept() 메서드가 새로운 소켓(client_socket)과 클라이언트의 주소(address)를 반환
			client_socket, address = self.server_socket.accept()
			print(f"새로운 연결: {address}")
			# 클라이언트와의 통신을 독립적으로 처리하기 위해 새로운 스레드를 생성하고, 
			# 해당 클라이언트를 처리하는 메서드인 handle_client를 실행
			client_thread = threading.Thread(
				# 클라이언트의 요청을 처리하는 메서드
				# 클라이언트의 메시지를 받고, 이를 다른 클라이언트들에게 브로드캐스트
				target=self.handle_client, args=(client_socket,)
			)
			client_thread.start()

	def handle_client(self, client_socket):
		name = "익명"
		# 클라이언트 소켓을 키로, 이름을 값으로 하여 self.clients 딕셔너리에 저장
		self.clients[client_socket] = name

		while True:
			try:
				# 클라이언트로부터 1024 바이트까지의 메시지를 수신하고 UTF-8로 디코딩하여 저장
				message = client_socket.recv(1024).decode("utf-8")
				if not message:
					break

				if message.startswith("/set name"):
					# /set name 명령어 뒤에 오는 새로운 이름을 추출하고, 양쪽 공백을 제거
					new_name = message[10:].strip()
					if new_name:
						# 이전 이름을 old_name에 저장하고, 
						# 클라이언트 딕셔너리에서 해당 클라이언트의 이름을 새로운 이름으로 업데이트
						old_name = self.clients[client_socket]
						self.clients[client_socket] = new_name
						# 모든 클라이언트에게 이름이 변경되었음을 브로드캐스트
						self.broadcast(
							f"{old_name}님이 {new_name}(으)로 이름을 변경했습니다."
						)
					else:
						# 이름 변경 명령이 아닐 경우, 일반 메시지로 간주하고 브로드캐스트
						self.broadcast(f"{self.clients[client_socket]}: {message}")

				# 클라이언트가 갑자기 연결을 끊으면 ConnectionResetError가 발생
				# 이 경우 예외를 처리하고 루프를 종료
			except ConnectionResetError:
				break

			# 클라이언트가 나가면, 해당 클라이언트를 self.clients 딕셔너리에서 삭제
			del self.clients[client_socket]
			# 클라이언트 소켓을 닫아 연결을 종료
			client_socket.close()
			# 라이언트가 채팅방을 떠났음을 모든 클라이언트에게 알
			self.broadcast(f"{name}님이 채팅방을 나갔습니다.")

	def broadcast(self, message):
		for client in self.clients:
			try:
				# self.clients 딕셔너리의 모든 클라이언트에게 메시지를 UTF-8로 인코딩하여 전송
				client.send(message.encode("utf-8"))
			except:
				pass


if __name__ == "__main__":
	server = ChatServer()
	server.start()
