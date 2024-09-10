import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("서버와의 연결이 끊어졌습니다.")
            break


def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

server_running = True

def handle_user_input():
        nonlocal server_running   
        while server_running:
            try:
                user_input = input().strip().lower()
                if user_input in ["q", "quit"]:
                    print("\n사용자 입력으로 서버 종료 중...")
                    server_running = False
                    break
            except EOFError:
                # Ctrl-C나 다른 이유로 EOFError가 발생하면 루프를 종료합니다.
                break
            except Exception as e:
                print(f"입력 처리 중 오류 발생: {e}")

def start_client():
    input_thread = threading.Thread(target=handle_user_input)  # 프로세스를 더 잘게 쪼갠 단위 thread. 동시에 처리할수 있게 쪼갬
    input_thread.daemon = True
    input_thread.start()

    try: 
        while server_running:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('localhost', 5000))

                receive_thread = threading.Thread(target=receive_messages, args=(client,))
                receive_thread.start()

                send_thread = threading.Thread(target=send_messages, args=(client,))
                send_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"연결 수락 중 오류 발생: {e}")
                if not server_running:
                    break
    except KeyboardInterrupt:
        print("\nCtrl-C로 서버 종료 중...")
    finally:
        server_running = False
        server_socket.close()
        print("서버가 종료되었습니다.")


if __name__ == "__main__":
    start_client()