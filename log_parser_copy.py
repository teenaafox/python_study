import re
import sys
from datetime import datetime
from collections import deque

def parse_log_file(file_path, num_lines):
    pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)'
    parsed_logs = deque(maxlen=num_lines)
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    # 타임존 정보를 제거하고 파싱 (Python 3.6 이하 버전 호환성을 위해)
                    # "2024-08-05T23:27:41+0900" 형식의 내용에서 뒤 5자리 +0900 제거
                    timestamp = datetime.strptime(timestamp_str[:-5], '%Y-%m-%dT%H:%M:%S')
                    parsed_logs.append({
                        'timestamp': timestamp,
                        'log_level': log_level,
                        'message': message.strip()
                    })
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except PermissionError:
        print(f"오류: '{file_path}' 파일을 읽을 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        sys.exit(1)
    
    return list(parsed_logs)

def main():
    if len(sys.argv) != 3:
        print("사용법: python log_parser.py <로그_파일_경로> <읽을_라인_수>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    try:
        num_lines = int(sys.argv[2])
        if num_lines <= 0:
            raise ValueError
    except ValueError:
        print("오류: 라인 수는 양의 정수여야 합니다.")
        sys.exit(1)

    parsed_logs = parse_log_file(log_file_path, num_lines)
    
    print(f"'{log_file_path}'에서 최근 {len(parsed_logs)}개의 로그 항목:")
    for log in parsed_logs:
        print(f"시간: {log['timestamp']}, 레벨: {log['log_level']}, 메시지: {log['message']}")

if __name__ == "__main__":
    main()