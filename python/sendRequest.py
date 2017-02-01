import sys
import os
import requests
import argparse
from os.path import join
import zipfile
import pexpect

"""
http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
"""


def zipDirectory(toFile, targetDirectory):
    with zipfile.ZipFile(toFile, 'w', zipfile.ZIP_DEFLATED) as f:
        for (dir, sub_dir, files) in os.walk(targetDirectory):
            f.write(dir)
            for file in files:
                f.write(os.path.join(dir, file))
     

def showResponseMsg(request):
    if request.status_code == requests.codes.ok:
        print(request.text)
    else:
        print(request.status_code)

url = 'http://localhost:18000/cgi-bin/receiveRequest.py'
#url = 'http://mm.cs.uec.ac.jp/narusawa-a/receiveRequest.py'

parser = argparse.ArgumentParser()
parser.add_argument('--src', '-s', default='src', help='working directory')
parser.add_argument('--res', '-r', default='res', help='resource directory')
parser.add_argument('--command', '-c', default=' ', help='proxy command')
parser.add_argument('--message', '-m', default=' ', help='message for description')
parser.add_argument('--id', help='identifier of local object')
parser.add_argument('--delete', '-d', action='store_true', help='delete object id')
parser.add_argument('--list', action='store_true', help='show objects')
parser.add_argument('--run', action='store_true', help='run specified id command')
parser.add_argument('--remote', default='/export/space/narusawa-a/_data/')

args = parser.parse_args()

_params = { }
_files = { }

_params['command'] = args.command
_params['message'] = args.message


if args.list:
    _params['mode'] = 'list'
    req = requests.get(url, params=_params)
    showResponseMsg(req)
    exit(0)





if not os.path.exists('.tmp'):
    os.mkdir('.tmp')

if os.path.exists(args.src):
    zipDirectory('.tmp/src.zip', args.src)
    _files['src'] = open('.tmp/src.zip', 'rb')


if os.path.exists(args.res):
    zipDirectory('.tmp/res.zip', args.res)
    _files['res'] = open('.tmp/res.zip', 'rb')


if args.id:
    _params['id'] = args.id

if args.run:
    assert args.id != None

    sys.exit(0)

if args.delete:
    assert args.id != None
    _params['mode'] = 'delete'
    req = requests.get(url, params=_params)
    showResponseMsg(req)
    exit(0)


"""
post requests
"""
if len(_files.keys()) == 0:
    r = requests.get(url, params=_params)
else:
    r = requests.post(url, files=_files, params=_params)

showResponseMsg(r)
