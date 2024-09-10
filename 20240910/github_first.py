import requests
import json


def get_github_repos(username, token):
    # GitHub API 엔드포인트
    url = f"https://api.github.com/users/{username}/repos"

    # 인증 헤더 설정
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        # GET 요청 보내기
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 오류 발생 시 예외 발생

        # JSON 응답 파싱
        repos = response.json()

        print(json.dumps(repos, indent=2, ensure_ascii=False))

        # 리포지토리 정보 출력
        print(f"{username}의 GitHub 리포지토리 목록:")
        for repo in repos:
            print(f"- {repo['name']}: {repo['html_url']}")

        return repos

    except requests.exceptions.RequestException as e:
        print(f"GitHub API 호출 중 오류 발생: {e}")
        return None


# 사용 예시
username = "아이디"
token = "토큰"

get_github_repos(username, token)