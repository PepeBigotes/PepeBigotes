#!/usr/bin/env python3
#I'm to lazy to change todo-list progress for emojis,
#so I wrote this script that replaces it automatically.
import re
print("===REPLACER.py===")

with open('README.md', 'r', encoding='utf-8') as readme:
    content = readme.read()
print('✔️')
print('!DONE  : ', content.count('!DONE'))
content = re.sub(r'!DONE', '✔️', content)

print('📝')
print('!INPROG: ', content.count('!INPROG'))
content = re.sub(r'!INPROG', '📝', content)

print('❌')
print('!NOPROG: ', content.count('!NOPROG'))
content = re.sub(r'!NOPROG', '❌', content)

with open('README.md', 'w', encoding='utf-8') as readme:
    readme.write(content)
    
print("===SCRIPT DONE!===")