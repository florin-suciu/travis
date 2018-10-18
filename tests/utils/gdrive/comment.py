import argparse
import json

import requests

TESTS_PASSED = "Tests passed - "


def remove_previous_comments(header, repo, pr, comment):
    """If the current comment is a Tests passed one, remove all previous Tests passed comments for this pr"""
    if not comment.startswith(TESTS_PASSED):
        return

    r = requests.get('https://api.github.com/repos/{}/issues/{}/comments'.format(repo, pr), headers=header)
    assert r.status_code == 200

    json_data = json.loads(r.content)
    to_delete = []
    for comment in json_data:
        if comment.get('body').startswith(TESTS_PASSED):
            to_delete.append(comment.get('id'))

    for comment_id in to_delete:
        r = requests.delete('https://api.github.com/repos/{}/issues/comments/{}'.format(repo, comment_id),
                            headers=header)
        assert r.status_code == 204


def post_comment(token, repo, pr, comment):
    header = {'Authorization': 'token {}'.format(token)}
    body = {"body": comment}

    remove_previous_comments(header, repo, pr, comment)

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
