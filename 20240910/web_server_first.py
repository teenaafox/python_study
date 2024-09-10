import socket
import os
import sys
from urllib.parse import unquote
import mimetypes
import threading


# 간단한 HTTP 서버를 구현하며, 
# 멀티스레딩을 사용하여 여러 클라이언트 요청을 동시에 처리할 수 있습니다. 
# 또한 사용자 입력을 통해 서버를 안전하게 종료할 수 있는 기능도 포함


# 주어진 파일 경로의 MIME 타입(예: text/html, image/png)을 추측합니다. 
# 알 수 없는 타입일 경우 "application/octet-stream"을 반환
def get_content_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"

# 클라이언트의 요청을 처리
# 클라이언트 소켓과 기본 디렉토리 경로를 인자로 받음
def handle_request(client_socket, base_dir):
    try:
        # 입력된 데이터를 처리하기 위한 초기 준비작업
        # 클라이언트로부터 요청을 받아 디코딩하고, 첫 번째 줄을 파싱
        request = client_socket.recv(1024).decode("utf-8")
        request_lines = request.split("\n")
        request_line = request_lines[0].strip().split()

        # HTTP 메소드와 요청 경로를 추출합니다. 경로는 URL 디코딩됩니다.
        if len(request_line) >= 2:
            method = request_line[0]     # HTTP 메서드(예: GET)
            path = unquote(request_line[1])    # 요청한 경로. 경로는 URL 인코딩된 문자가 있을 수 있기 때문에 unquote로 디코딩

            # GET 요청을 처리하며, 루트 경로 요청은 index.html로 리다이렉트
            if method == "GET":
                if path == "/":
                    path = "/index.html"

                try:
                    # 요청된 파일을 읽고, 적절한 HTTP 응답을 생성
                    # 요청한 파일이 존재하면 파일을 열고 그 내용을 클라이언트에게 보냅니다. 
                    # MIME 타입을 파일 확장자를 통해 추측하고, 파일을 읽어 응답 메시지에 포함시킵니다
                    file_path = os.path.join(base_dir, path.lstrip("/"))
                    with open(file_path, "rb") as file:
                        content = file.read()
                    content_type = get_content_type(file_path)
                    response = (
                        f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}; charset=utf-8\r\n\r\n".encode()
                        + content
                    )
                except FileNotFoundError:
                             # 항상 쓰는 HTTP 응답 규칙 : HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>404 Not Found</h1>".encode(
                        "utf-8"
                    )
            else:
                response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>405 Method Not Allowed</h1>".encode(
                    "utf-8"
                )
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>400 Bad Request</h1>".encode(
                "utf-8"
            )

        # 생성된 응답을 클라이언트에게 전송
        client_socket.sendall(response)

    # # 예외 처리 및 소켓 닫기를 수행
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()


# 포트(외부) == 소켓(내부)
# 서버를 실행하는 메인 함수
def run_server(base_dir, port=8080):
    # 서버 소켓을 생성하고 설정
    # 서버 소켓을 설정하고, 포트 번호로 서버를 바인딩한 후 연결을 대기
    # 타임아웃을 1초로 설정해 서버가 입력을 기다리는 동안 무한 대기를 하지 않게 합니다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 웹서버 동작 초기화
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 웹서버 동작 초기화
    server_socket.bind(("", port))   # 내 피씨와 포트를 바인드. 연결
    server_socket.listen(1)          # 요청이 오면 listen
    server_socket.settimeout(1)      # 1초 타임아웃 설정

    # 서버 실행 정보를 출력
    print(f"서버가 http://localhost:{port}/에서 실행 중입니다.")
    print(f"서빙 디렉토리: {base_dir}")
    print("서버를 종료하려면 'q' 또는 'quit'를 입력하거나 Ctrl-C를 누르세요.")

    # 사용자 입력을 처리하는 함수입니다. 'q' 또는 'quit' 입력 시 서버를 종료
    # 서버 종료를 위해 사용자 입력을 기다리는 쓰레드를 실행
    server_running = True

    def handle_user_input():
        nonlocal server_running   # nonlocal 써야하는 이유: 함수 밖에서 쓴 변수는 밖의 것으로 안의 것은 안으로 인식하는데, 밖에 선언하고 함수 안에서 쓰고 싶을때 nonlocal dmf TJwnsek
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

    # 즉시 실행 함수는 () 표시, 이런 함수가 있다 필요할때 실행해 하는 함수는 () 생략
    # 사용자 입력 처리를 위한 별도의 스레드를 생성하고 시작
    input_thread = threading.Thread(target=handle_user_input)  # 프로세스를 더 잘게 쪼갠 단위 thread. 동시에 처리할수 있게 쪼갬
    input_thread.daemon = True
    input_thread.start()

    # 메인 서버 루프입니다. 클라이언트 연결을 받아 각 요청을 별도의 스레드에서 처리
    # 클라이언트 연결을 기다리며 요청이 들어오면 새로운 쓰레드로 요청을 처리
    try:
        while server_running:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"연결됨: {client_address}")
                client_thread = threading.Thread(
                    target=handle_request, args=(client_socket, base_dir)
                )
                client_thread.start()
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


# 메인 함수입니다. 커맨드 라인 인자를 파싱하고, 서버를 실행합니다. 스크립트가 직접 실행될 때만 main() 함수를 호출
def main():
    if len(sys.argv) != 2:
        print("사용법: python webserver.py <directory_path>")
        sys.exit(1)

    base_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isdir(base_dir):
        print(f"오류: {base_dir}는 유효한 디렉토리가 아닙니다.")
        sys.exit(1)

    # 유효한 디렉토리 경로가 제공되면 서버를 실행
    run_server(base_dir)


if __name__ == "__main__":
    main()