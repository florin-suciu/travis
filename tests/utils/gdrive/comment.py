import argparse

import requests


def post_comment(token, repo, pr, comment):
    header = {'Authorization': 'token {}'.format(token)}
    body = {"body": comment}
    r = requests.post('https://api.github.com/repos/{}/issues/{}/comments'.format(repo, pr), headers=header, json=body)
    assert r.status_code == 201


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('auth_token')
    parser.add_argument('repo')
    parser.add_argument('pr')
    parser.add_argument('comment')
    args = parser.parse_args()
    post_comment(args.auth_token, args.repo, args.pr, args.comment)
