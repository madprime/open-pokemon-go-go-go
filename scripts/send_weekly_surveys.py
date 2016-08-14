import argparse
import sys

import requests


def send_mail(token, email_filepath, member_filepath):
    members = []
    with open(member_filepath) as member_file:
        for line in member_file:
            members.append(line.strip())
    message = ''
    with open(email_filepath) as email_file:
        message = ''.join(email_file.readlines())
    url = ('https://www.openhumans.org/api/direct-sharing/project/message/'
           '?access_token={}'.format(token))
    params = {'all_members': False,
              'message': message,
              'project_member_ids': members
              }
    req = requests.post(url, data=params)
    print(req.status_code)
    print(req.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send weekly surveys.')
    parser.add_argument('--token', metavar='MASTERTOKEN',
                        help='Open Humans project master access token')
    parser.add_argument('--email', metavar='EMAILFILE',
                        help='text of email to send')
    parser.add_argument('--members', metavar='MEMBERFILE',
                        help='text file containing list of member IDs')
    args = parser.parse_args()
    print(args.token)
    print(args.email)
    print(args.members)
    send_mail(token=args.token,
              email_filepath=args.email,
              member_filepath=args.members)
