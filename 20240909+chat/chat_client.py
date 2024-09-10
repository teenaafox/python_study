import socket    # 네트워크 소켓을 다루기 위해 socket 모듈을 임포트 / 소켓을 사용하면 컴퓨터 간에 데이터를 주고받을 수 있
import threading # 멀티스레딩을 위해 threading 모듈을 임포트 / 여러 작업을 동시에 처리할 수 있도록 스레드를 사용

# 클라이언트는 서버에 연결하고 두 개의 스레드를 만듭니다. 
# 하나는 서버로부터 메시지를 받는 역할을 하고, 다른 하나는 서버에 메시지를 보내는 역할을 합니다.

# 서버에서 오는 메시지를 계속해서 받을 함수
def receive_messages(client_socket):
	while True:   # 무한 루프를 통해 클라이언트가 서버에서 받은 메시지를 계속 수신
		try:
			# 서버에서 보내온 메시지를 1024바이트까지 받습니다. (1024는 버퍼 크기)
			# 받은 메시지를 UTF-8로 디코딩하여 출력
			message = client_socket.recv(1024).decode('utf-8')
			print(message)
		except:
			print("서버와의 연결이 끊어졌습니다.")
			break


# 클라이언트가 서버로 메시지를 보낼 수 있는 함수
def send_messages(client_socket):
	while True:  # 무한 루프에서 사용자가 입력한 메시지를 계속해서 서버에 보낸다
		# 사용자로부터 입력을 받고, 이를 UTF-8로 인코딩하여 서버로 전송
		message = input()
		client_socket.send(message.encode('utf-8'))  # client_socket.send():서버에 데이터를 전송하는 소켓의 메소드


# 클라이언트 연결을 시작하고, 메시지 송수신 스레드를 시작하는 함수
def start_client():
	# 새로운 소켓 객체를 생성
	# AF_INET은 IPv4 주소 체계를 사용한다는 의미
	# SOCK_STREAM은 TCP 프로토콜을 사용하여 신뢰성 있는 데이터 스트림을 의미
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# localhost의 5000번 포트에 연결을 시도. 이 연결은 클라이언트가 서버와 통신할 준비가 되었음을 의미
	client.connect(('localhost', 5000))

	# 서버로부터 메시지를 받기 위한 새로운 스레드를 생성
	# target=receive_messages로 이 스레드가 receive_messages 함수를 실행하도록 설정
	# args=(client,)로 클라이언트 소켓을 이 함수의 인수로 전달
	receive_thread = threading.Thread(target=receive_messages, args=(client,))
	# 생성한 스레드를 시작하여 서버로부터 메시지를 수신하기 시작
	receive_thread.start()

	# 메시지를 보내기 위한 새로운 스레드를 생성
	# send_messages 함수가 실행되도록 설정하고, 클라이언트 소켓을 인수로 전달
	send_thread = threading.Thread(target=send_messages, args=(client,))
	# 생성한 스레드를 시작하여 클라이언트가 서버로 메시지를 보낼 수 있게 합
	send_thread.start()


if __name__ == "__main__":
	start_client()    # 클라이언트를 시작하고 메시지 송수신 스레드를 동작