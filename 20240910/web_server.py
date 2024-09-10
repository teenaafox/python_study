import socket
import os
import sys
from urllib.parse import unquote
import mimetypes
import threading

def get_content_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


def handle_request(client_socket, base_dir):
    try:
        request = client_socket.recv(1024).decode("utf-8")
        request_lines = request.split("\n")
        request_line = request_lines[0].strip().split()

        if len(request_line) >= 2:
            method = request_line[0]
            path = unquote(request_line[1])
            
            if method == "GET":
                if path == "/":
                    path = "/index.html"
                
                try:
                    file_path = os.path.join(base_dir, path.lstrip("/"))
                    with open(file_path, "rb") as file:
                        content = file.read()
                    content_type = get_content_type(file_path)
                    response = (
                        f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}, charset=utf-8\r\n\r\n".encode() 
                        + content
                    )
                except FileNotFoundError:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>404 Not Found</h1>".encode("utf-8")
            else:
                response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>405 Method Not Allowed</h1>".encode("utf-8")
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>400 Bad Request</h1>".encode("utf-8")
        
        client_socket.sendall(response)

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()


def run_server(base_dir, port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(1)
    server_socket.settimeout(1)

    print(f"서버가 http://localhost:{port}/에서 실행 중입니다.")
    print(f"서빙 디렉토리: {base_dir}")
    print("서버를 종료하려면 'q' 또는 'quit'를 입력하거나 Ctrl+C를 누르세요.")

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
                break
            except Exception as e:
                print(f"입력 처리 중 오류 발생: {e}")

    input_thread = threading.Thread(target=handle_user_input)
    input_thread.daemon = True
    input_thread.start()

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


def main():
    if len(sys.argv) != 2:
        print("사용법: python webserver.py <directory_path>")
        sys.exit(1)

    base_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isdir(base_dir):
        print(f"오류: {base_dir}는 유효한 디렉토리가 아닙니다.")
        sys.exit(1)

    run_server(base_dir)


if __name__ == "__main__":
    main()