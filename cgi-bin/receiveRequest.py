#!/Volumes/MacintoshHD3/Homebrew//bin/python3
import sys
import os
from os.path import join
import cgi
import uuid
import json
import zipfile

form = cgi.FieldStorage()

print('Content-Type: text/html; charset="utf-8" \n')

prefix = './data'
desc = dict()

if not os.path.exists(os.path.join(prefix, 'index')):
    os.makedirs(os.path.join(prefix, 'index'))

if form.keys().__contains__('id'):
    id = form['id'].value

else:
    id = str(uuid.uuid4()).split('-')[0]
    if not os.path.exists(join(prefix, id)):
        os.makedirs(join(prefix, id))

desc['id'] = id

def showList():
    for jsonFile in os.listdir(join(prefix, 'index')):
        jsonFile = join(prefix, 'index', jsonFile)
        with open(jsonFile, 'r') as f:
            data = json.load(f)
            str1 = 'id: {} command: {} '.format(data['id'], data['command'])
            str2 = ' msg : {}'.format(data['message'])
            print(str1)
            print(str2)

def deleteItem():
    file = join(prefix, 'index', 'id_{}.json'.format(id))
    if os.path.exists(file):
        os.remove(file)
        print('removed id: {}'.format(id))
    else:
        print('No such a Id!')

def extractDirectory(keyword):
    if form.keys().__contains__(keyword):
        filename = join(prefix, id, 'tmp.zip')
        f = open(filename, 'wb')
        f.write(form[keyword].value)
        f.close()
        with zipfile.ZipFile(filename, 'r') as f:
            f.extractall(join(prefix, id))



if form.keys().__contains__('mode'):
    if form['mode'].value == 'list':
        showList()
    if form['mode'].value == 'delete' and form.keys().__contains__('id'):
       deleteItem()

    sys.exit(0)


extractDirectory('src')
extractDirectory('res')



"""
dump infomation with json format.
"""

desc['command'] = form['command'].value
desc['message'] = form['message'].value

indexWriter = open(join(prefix, 'index', 'id_{}.json'.format(id)), 'w')
json.dump(desc, indexWriter, indent=3)
indexWriter.close()