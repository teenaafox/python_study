"""
're'는 로그 라인에서 정보를 추출하는 데 사용됩니다.
'sys'는 스크립트 실행 중 오류 처리나 종료에 사용될 수 있습니다.
'datetime'은 로그의 타임스탬프를 파싱하고 조작하는 데 사용됩니다.
'deque'는 효율적으로 로그 항목을 저장하고 관리하는 데 사용될 수 있습니다.
"""
import re        # 정규표현식 모듈인 're' : 문자열 패턴 매칭과 처리에 사용
import sys       # 시스템 관련 파라미터와 함수를 제공하는 'sys' 모듈 - 스크립트 종료나 명령줄 인수 처리 등에 사용
from datetime import datetime  # 'datetime' 모듈에서 'datetime' 클래스 - 이 클래스는 날짜와 시간을 다루는 데 사용
from collections import deque  # 'collections' 모듈에서 'deque'(double-ended queue) 클래스 - deque는 양쪽 끝에서 빠르게 요소를 추가하거나 제거할 수 있는 리스트 형태의 컨테이너

def parse_log_file(file_path, num_lines):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)"
    parsed_logs = deque(maxlen=num_lines)

    try:
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()

                    # 문자열을 datetime 객체로 변환
                    # 문자열의 형식을 지정하여 날짜와 시간 정보를 파싱
                    timestamp = datetime.strptime(
                        timestamp_str[:-5], "%Y-%m-%dT%H:%M:%S"
                    )

                    # datetime 객체를 문자열로 변환
                    # 원하는 형식의 문자열로 날짜와 시간을 포맷팅
                    # %p는 AM/PM을 표시
                    # %I는 12시간 형식으로 시간을 표시
                    formatted_date = timestamp.strftime("%y년 %m월 %d일 %p %I시 %M분 %S초")
                    formatted_date = formatted_date.replace("AM", "오전").replace("PM", "오후")

                    # 월, 일, 시간 앞의 불필요한 0 제거
                    formatted_date = re.sub(r'0(\d월)', r'\1', formatted_date)
                    formatted_date = re.sub(r'0(\d일)', r'\1', formatted_date)
                    formatted_date = re.sub(r'0(\d시)', r'\1', formatted_date)

                    parsed_logs.append(
                        {
                            "timestamp": formatted_date,
                            "log_level": log_level,
                            "message": message.strip(),
                        }
                    )
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


def create_html_content(parsed_logs):
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>로그 파서 결과</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>파싱된 로그</h1>
        <table>
            <tr>
                <th>시간</th>
                <th>로그 레벨</th>
                <th>메시지</th>
            </tr>
    """

    for log in parsed_logs:
        html_content += f"""
            <tr>
                <td>{log['timestamp']}</td>
                <td>{log['log_level']}</td>
                <td>{log['message']}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """

    return html_content


def main():
    if len(sys.argv) != 4:
        print(
            "사용법: python log2html/.py <로그_파일_경로> <읽을_라인_수> <출력_HTML_파일_경로>"
        )
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    output_html_path = sys.argv[3]

    try:
        num_lines = int(sys.argv[2])
        if num_lines <= 0:
            raise ValueError
    except ValueError:
        print("오류: 라인 수는 양의 정수여야 합니다.")
        sys.exit(1)

    parsed_logs = parse_log_file(log_file_path, num_lines)

    html_content = create_html_content(parsed_logs)

    try:
        with open(output_html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        print(f"HTML 파일이 성공적으로 생성되었습니다: {output_html_path}")
    except PermissionError:
        print(f"오류: '{output_html_path}'에 쓸 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"HTML 파일 생성 중 오류 발생: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
