import re
import sys
from datetime import datetime
from collections import deque


def parse_log_file(file_path, num_lines):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)"
    parsed_logs = deque(maxlen=num_lines)

    try:
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    timestamp = datetime.strptime(
                        timestamp_str[:-5], "%Y-%m-%dT%H:%M:%S"
                    )
                    parsed_logs.append(
                        {
                            "timestamp": timestamp,
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
            "사용법: python log_parser.py <로그_파일_경로> <읽을_라인_수> <출력_HTML_파일_경로>"
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