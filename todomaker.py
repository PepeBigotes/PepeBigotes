#!/usr/bin/env python3
#I want to have my own todo-list format.
#This script transfers that format to the markdown file.
#Pepe's TodoList Language maybe?
print("======TODOMAKER.py======")


#=PART 0: Imports, constants and defs

import time
import inspect


README = "README.md" #Markdown file where the table is located
README_START_KEYWORD = "<!--TODOLIST-->"
README_END_KEYWORD = "<!--/TODOLIST-->"

TODOLIST = "todolist.txt" #Text file similar to XML containing the tasks data
TODOLIST_START_KEYWORD = "<TASK>"
TODOLIST_END_KEYWORD = "</TASK>"


def get_var_name(input):
    for name, value in locals().items():
        if value is input:
            return name
    return None


#=PART 1: Detect and store tasks data from todolist.txt

start_keyword = TODOLIST_START_KEYWORD
end_keyword = TODOLIST_END_KEYWORD


tasks = []
task_content = []
start_index = None
end_index = None


print(f"Stripping values from {TODOLIST}...")
with open(TODOLIST, 'r', encoding='utf-8') as file:
    for line in file:
        if start_keyword in line:
            task_content = []
            for line in file:
                if end_keyword in line:
                    tasks.append(task_content)
                    break
                task_content.append(line.strip())
                print("└Strip: ", line.strip())

if tasks:
    print(f'The task contents are:')
    for line in tasks:
        print(f"└{line}")
else:
    if start_index is not None:
        print(f"[ERROR] No {end_keyword} in {TODOLIST}")
    elif end_keyword is not None:
        print(f"[ERROR] No {start_keyword} in {TODOLIST}")
    else:
        print(f"[ERROR] No {start_keyword} nor {end_keyword} in {TODOLIST}")
           
    print("   Check your syntax, bozo")
    exit()
    
print()


#=PART 2: Transform data to markdown format

if len(tasks) > 0:
    print(f"Transforming {len(tasks)} tasks...")
    for task in range(0, len(tasks)):
        print(f"# TASK {task}:")
        print(tasks[task][0])
        tasks[task][0] = f'<tr>\n<td align="center">{tasks[task][0]}</td>\n'
        
        print(tasks[task][1])
        tasks[task][1] = f'<td>{tasks[task][1]}</td>\n'
        
        print(tasks[task][2])
        tasks[task][2] = f'<td><a href="{tasks[task][2]}">\n'
        
        print(tasks[task][3])
        tasks[task][3] = f'{tasks[task][3]}</a></td>\n</tr>\n'
        print()
else:
    print(f"[ERROR] No tasks detected in {TODOLIST}")
    exit()

print()


#=PART 3: Detect and delete current TodoList from .md

start_keyword = README_START_KEYWORD
end_keyword = README_END_KEYWORD


with open(README, "r", encoding='utf-8') as file:
    lines = file.readlines()


start_index = None
end_index = None

for i in range(len(lines)):
    if start_keyword in lines[i]:
        start_index = i
        print("Detected ", start_keyword , " at line ", start_index +1)
    elif end_keyword in lines[i]:
        end_index = i
        print("Detected ", end_keyword , " at line ", end_index +1)
        break


if start_index and end_index:
    lines_deleted = end_index - start_index -1
    if lines_deleted <= 0:
        print("[ERROR] No lines were deleted")
    else:
        del lines[start_index + 1 : end_index]
        with open(README, "w", encoding='utf-8') as file:
            file.writelines(lines)
        print(f"Deleted {lines_deleted} lines")
else:
    if start_index:
        print(f"[ERROR] No {end_keyword} in {README}")
    elif end_index:
        print(f"[ERROR] No {start_keyword} in {README}")
    else:
        print(f"[ERROR] No {start_keyword} nor {end_keyword} in {README}")
        
    print("   Check your syntax, bozo")

print()


#=PART 4: Write new TodoList table to .md

prefix = [ \
    "<table align='center'>\n", \
    "<tr>\n", \
    "<th><b>Progress</b></th>\n", \
    "<th><b>Task</b></th>\n", \
    "<th><b>Repo</b></th>\n", \
    "</tr>\n", \
]
sufix = ["</table>\n"]


final_table = prefix + tasks + sufix
lines[start_index + 1 : start_index + 1] = final_table


with open(README, 'w', encoding='utf-8') as file:
    print("Writing contents to markdown file...")
    for line in lines:
        if isinstance(line , list):
            for i in line:
                file.write(i)
        else:   
            file.write(line)


print()
print("===TODOMAKER.PY OVER!===")