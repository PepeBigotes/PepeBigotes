#!/usr/bin/env python3
#I'm to lazy to change todo-list progress for emojis,
#so I wrote this script that replaces it automatically.
print("======REPLACER.py======")


FILE_PATH = "README.md"


import re

def replace(from_this , to_this):
    global content
    content = re.sub(from_this, to_this , content)
    

with open(FILE_PATH, 'r', encoding='utf-8') as readme:
    print("Reading file...")
    content = readme.read()


print('┌✔️')
print('└!DONE  : ', content.count('!DONE'))
print('┌📝')
print('└!INPROG: ', content.count('!INPROG'))
print('┌❌')
print('└!NOPROG: ', content.count('!NOPROG'))


replace('!DONE', '✔️')
replace('!INPROG', '📝')
replace('!NOPROG', '❌')


with open(FILE_PATH, 'w', encoding='utf-8') as readme:
    readme.write(content)


print("===REPLACER.PY DONE!===")