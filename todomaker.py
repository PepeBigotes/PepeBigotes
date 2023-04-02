#!/usr/bin/env python3
#I want to have my own todo-list format.
#This script transfers that format to the markdown file.
#Pepe's TodoList Language maybe?

#=PART 0: Imports and variables
import time

readme = "README.md"
todolist = "todolist.txt"

#=PART 1: Detect and delete current TodoList from .md
start_keyword = "<!--TODOLIST-->"
end_keyword = "<!--/TODOLIST-->"

with open(readme, "r", encoding='utf-8') as file:
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

if start_index is not None and end_index is not None:
    lines_deleted = end_index - start_index -1
    if lines_deleted <= 0:
        print("No lines were deleted")
    else:         
        del lines[start_index + 1 : end_index]
        with open(readme, "w", encoding='utf-8') as file:
            file.writelines(lines)
        print(f"Deleted {lines_deleted} lines")
else:
    if start_index is not None:
        print(f"No {end_index} in {readme}")
    elif end_index is not None:
        print(f"No {start_index} in {readme}")
    else:
        print(f"No {start_keyword} nor {end_keyword} in {readme}")
        
    print("Check your syntax, bozo")

print()
#=PART 2: Detect and store values from todolist.txt

start_keyword = '<TASK>'
end_keyword = '</TASK>'
tasks = []
task_content = []

print(f"Stripping values from {todolist}...")
with open(todolist, 'r', encoding='utf-8') as file:
    for line in file:
        if start_keyword in line:
            task_content = []
            for line in file:
                if end_keyword in line:
                    tasks.append(task_content)
                    break
                task_content.append(line.strip())
                print("Strip: ", line.strip())

if tasks:
    print(f'The lines between {start_keyword} and {end_keyword} are:')
    for line in tasks:
        print(line)
else:
    if start_index is not None:
        print(f"No {end_keyword} in {readme}")
    elif end_keyword is not None:
        print(f"No {start_keyword} in {readme}")
    else:
        print(f"No {start_keyword} nor {end_keyword} in {readme}")
        
    print("Check your syntax, bozo")
    
print()
#=PART 3: Transform values to markdown format
if len(tasks) > 0:
    print(f"Transforming {len(tasks)} tasks...")
    for task in range(0, len(tasks)):
        print(f"TASK {task}:")
        tasks[task][0] = f'<td align="center">{tasks[task][0]}</td>\n'
        print(tasks[task][0])
        
        tasks[task][1] = f'<td>{tasks[task][1]}</td>\n'
        print(tasks[task][1])
        
        tasks[task][2] = f'<td><a href="{tasks[task][2]}">\n'
        print(tasks[task][2])
        
        tasks[task][3] = f'{tasks[task][3]}"</a></td>\n'
        print(tasks[task][3])
else:
    print(f"No tasks detected in {todolist}")

print()
#=PART 4: Write new TodoList to .md

prefix = [ \
    "<table align='center'>\n", \
    "<tr>\n", \
    "<th><b>Progress</b></th>\n", \
    "<th><b>Task</b></th>\n", \
    "<th><b>Repo</b></th>\n", \
    "</tr>\n", \
]
sufix = ["</table>"]

final_table = prefix + tasks + sufix

for i in range(len(final_table)):
    final_table[i] = [line + "\n" for line in final_table[i]]
    
lines.insert(start_index + 1, final_table)

for i, element in enumerate(final_table):
    lines = [str(line) for line in lines]
    file.write("".join(lines))

with open(readme, 'w', encoding='utf-8') as file:
    file.write("".join(lines))
    
print("SCRIPT OVER!")