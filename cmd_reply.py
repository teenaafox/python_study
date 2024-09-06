import subprocess
import sys

def run_command(command):
    """
    주어진 명령어를 실행하고 그 결과를 반환합니다.

    :param command: 실행할 쉘 명령어
    :return: 명령어 실행 성공 여부 (True/False)
    """
    try:
        print(f"명령어 실행 중: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("출력:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"명령어 '{command}' 실행 중 오류 발생: {e}")
        print("오류 출력:", e.stderr)
        return False

def read_commands_from_file(filename):
    """
    지정된 파일에서 명령어을 읽어옵니다.

    :param filename: 명령어가 저장된 파일의 경로
    :return: 명령어 리스트 또는 오류 시 None
    """
    try:
        # 빈 줄이나 주석이 포함된 줄을 제외하고, 파일의 각 줄을 리스트로 반환
        with open(filename, 'r') as file:

            # 리스트 내포(list comprehension)를 사용하여 파일의 각 줄(line)을 순회하며 처리
            # 리스트 내포란? 
            # 리스트를 간결하고 효율적으로 생성하는 방법 중 하나
            # = 반복문과 조건문을 한 줄로 작성하여 리스트를 만들 수 있다
            # 기본 형태:      [표현식 for 항목 in 반복 가능한 객체]
            # 조건 추가 형태: [표현식 for 항목 in 반복 가능한 객체 if 조건]
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except IOError as e:
        print(f"파일 {filename} 읽기 오류: {e}")
        return None
    
def execute_commands_sequentially(commands):
    """
    주어진 명령어 리스트를 순차적으로 실행합니다.

    :param commands: 실행할 명령어 리스트
    :return: 모든 명령어 실행 성공 여부 (True/False)
    """
    for cmd in commands:
        success = run_command(cmd)
        if not success:
            print(f"명령어 실행 실패. 시퀀스를 중단합니다.")
            return False
        print(f"명령어가 성공적으로 완료되었습니다. 다음 명령어로 이동합니다.\n")
    return True

def main(command_file):
    """
    메인 실행 함수: 파일에서 명령어를 읽고 순차적으로 실행합니다.

    :param command_file: 명령어가 저장된 파일의 경로

    사용예시: 아래 내용처럼 명령어를 순서대로 나열하여 저장합니다. 예) cmds.txt

    # System check commands
    echo 'Step 1: 디스크 용량 확인'
    df -h
    echo 'Step 2: 메모리 사용량 확인'
    free -m
    echo 'Step 3: 시스템 가동시간 확인'
    uptime
    """

    print(f"파일에서 명령어 읽는 중: {command_file}")
    commands = read_commands_from_file(command_file)

    if commands is None:
        print("명령어를 읽는데 실패했습니다. 종료합니다.")
        sys.exit(1)

    if not commands:
        print("파일에서 명령어를 찾을 수 없습니다. 종료합니다.")
        sys.exit(0)
    
    print(f"실행할 명령어 {len(commands)}개를 찾았습니다.")
    print("순차적 명령어 실행을 시작합니다...")

    if execute_commands_sequentially(commands):
        print("모든 명령어가 성공적으로 실행되었습니다.")
    else:
        print("오류로 인해 명령어 시퀀스가 중단되었습니다.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python script.py <명령어_파일>")
        sys.exit(1)

    command_file = sys.argv[1]
    main(command_file)