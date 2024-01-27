#!/usr/bin/env python3
#Created by PepeBigotes



#0. Constants

README = "README.md" #Markdown file where to paste the ToDo table
README_START_KEYWORD = "<!--TODOLIST-->"
README_END_KEYWORD = "<!--/TODOLIST-->"

TODOLIST = "todolist.yml" # YML file containing the tasks data (check 'example-tasks.yml' for reference)
TODOLIST_START_KEYWORD = "TASK"
TODOLIST_END_KEYWORD = "</TASK>"

URL_PREFIX = "https://github.com" # To avoid typing the full URL every time

PROG_KEYWORDS = {
    'not-started': '❌', # Not started
    'started': '📝', # Started
    'done': '✔️', # Done
}



#1. Funcs / Utils / Classes

def clear_strings(string, mode=True):
# Input:  "parameter: 'damn a string' #comment here"
    quotes = ['"', "'"]
    this_quote = quotes
    is_string = False
    output = '' # Output: "parameter:                 #comment here"
    s_output = [] # Output: ['damn a string']
    var = ''
    for char in string:
        if char in this_quote:
            this_quote = quotes if is_string else char
            is_string = not is_string

        if not is_string and char in quotes:
            output += ' '
            continue
        if mode:
            output += ' ' if is_string else char
        if not mode:
            if not is_string and len(var) > 0:
                s_output.append(var)
                var = ''
            if char in this_quote: continue
            if is_string: var += char

    if len(var) > 0: s_output.append(var)

    if mode: return output # input cleared of strings
    if not mode: return s_output # list of strings in input

class YML(): # My own YML parser, what could go wrong?
    def __init__(self, filepath):
        content = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file: content.append(line)
        except PermissionError:
            print(f"[!] Permission error when reading {TODOLIST}\nIs the file read protected?")
            exit()
        content = [i.rstrip("\n") for i in content]
        objects = []
        now_object = None

        for line in content: # Delete comments (ignores if inside strings)
            if len(line) == 0: continue
            clear_line = clear_strings(line)
            if '#' in clear_line:
                uncommented_line = ''
                for char in clear_line:
                    if char == '#': break
                    uncommented_line += char                    
                content[content.index(line)] = uncommented_line

        content = [i.rstrip(' ') for i in content] # Delete redundant spaces
        for line in content[::-1]: # Delete blank lines
            if line == "": content.pop(content.index(line))

        #for i in content: print(f"[debug] {i}")

        for line in content: # Parse content to object
            clear_line = clear_strings(line)
            strings = clear_strings(line, False)
            if line[0] != ' ':
                if now_object:
                    for key in now_object.keys():
                        value = now_object.get(key)
                        if len(value) == 1: now_object[key] = value[0] # Lists with only one item? cringe
                    objects.append(now_object)
                now_object = {}
                now_object['name'] = line.split(':')[0]
                continue

            now_par = clear_line.split(':')[0].lstrip(' ')
            now_val = strings
            #print(f"[debug] PAR:{now_par}, VAL:{now_val}")
            #print(f"[debug] {now_object}")

            if not now_par and not now_val:
                print(f"Undefined YML object parameter and value at line: '{line}'\ncheck your syntax in '{filepath}', bozo")
                exit()
            if not now_par:
                print(f"Undefined YML object parameter at line: '{line}'\ncheck your syntax in '{filepath}', bozo")
                exit()
            if not now_val:
                print(f"Undefined YML '{now_par}' value at line: '{line}'\ncheck your syntax in '{filepath}', bozo")
                exit()
            if (not '"' in line) and (not "'" in line):
                for i in now_val:
                    now_val[now_val.index(i)] = eval(i)
            now_object[now_par] = now_val
        objects.append(now_object)

        #print(f"[debug] CONTENT: {content}")
        #print(f"[debug] OBJECTS {objects}")
        self.content = tuple(content) # YML text lines, cleared of comments, empty lines and spaces
        self.objects = tuple(objects) # Dictionaries




#2. Read TODOLIST file (and validate task data)

yml_objects = YML(TODOLIST).objects

if not yml_objects:
    print(f"[!] Couldn't find any YML objects in '{TODOLIST}'\ncheck your syntax, bozo")
    exit()
print(f"[✓] Readed {len(yml_objects)} tasks from {TODOLIST}")

tasks = []
for obj in yml_objects:
    name = obj.get('name')
    prog = obj.get('prog', "-")[0]
    repo = obj.get('repo', "-")[0]
    tasks.append({'name': name, 'prog': prog, 'repo': repo})
"""
print("[debug] TASKS:")
for task in tasks:
    print(task.get('name'))
    print(task.get('prog'))
    print(task.get('repo'))
"""



#4. Read README file

readme = []
try:
    with open(README, 'r', encoding='utf-8') as file:
        for line in file: readme.append(line.rstrip('\n'))
    print(f"[✓] Readed {len(readme)} lines from {README}")
except PermissionError:
    print(f"[!] Permission error when reading {README}\nIs the file read protected?")
    exit()
try:
    start_index = readme.index(README_START_KEYWORD) +1
    end_index = readme.index(README_END_KEYWORD)
    print(f"[✓] Detected todolist tags at lines {start_index} and {end_index+1} in {README}")
except ValueError:
    print(f"[!] {README} lacks {README_START_KEYWORD}, {README_END_KEYWORD}, or both\ncheck your syntax, bozo")
    exit()

foo = []
ignore = False
for i in readme:
    if i == README_START_KEYWORD: ignore = True; foo.append(i); continue
    if i == README_END_KEYWORD: ignore = False
    if not ignore: foo.append(i)

readme = foo



#3. Prepare tasks data (+replace keywords for icons)

tasks_table = [
    "  <table align='center'>",
    "    <tr>",
    "      <th><b>Progress</b></th>",
    "      <th><b>Task</b></th>",
    "      <th><b>Repo</b></th>",
    "    </tr>",
]

for task in tasks:
    name = task.get('name')
    prog = task.get('prog')
    repo = task.get('repo')
    repo_url = f"<a href='{URL_PREFIX}{repo}'>{repo}</a>" if len(repo) > 1 else '-'

    tasks_table.append("    <tr>")
    tasks_table.append(f"      <td align='center'>{prog}</td>")
    tasks_table.append(f"      <td>{name}</td>")
    tasks_table.append(f"      <td>{repo_url}</td>")
    tasks_table.append("    </tr>")
tasks_table.append("  </table>")

for i in range(len(tasks_table)): tasks_table[i] += '\n'

print(f"[✓] Created a task table of {len(tasks_table)} lines")

from re import sub as replace

for i in PROG_KEYWORDS.keys():
    count = 0
    for line in tasks_table: # Could be more optimized, cry about it
        if i in line: count += 1
    #print(f"[debug] {i} count: {count}")
    if count == 0: continue
    for x in range(len(tasks_table)):
        tasks_table[x] = replace(i, PROG_KEYWORDS[i], tasks_table[x])
    print(f"[✓] Replaced {count} {i} for {PROG_KEYWORDS[i]}")

#for i in tasks_table: print(f"[debug] {i}")

for i in range(len(readme)): readme[i] += '\n'
readme[start_index:start_index] = tasks_table

#for i in readme: print(f"[debug] {i}", end='')



#5. Write ToDo table to README file

try:
    with open(README, 'w', encoding='utf-8') as file:
        for line in readme: file.write(line)
    print(f"[✓] Wrote {len(readme)} lines to {README}")
except PermissionError:
    print(f"[!] Permission error when writing to {README}\nIs the file write protected?")
    exit()