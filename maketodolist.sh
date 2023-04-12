#!/bin/bash
#I'm once again too lazy to execute both scripts.
#So this script does that for me.

echo "Creating todo list..."
echo
py -3 todomaker.py
echo
echo "Replacing for emojis..."
echo
py -3 replacer.py
echo
echo "MakeTodoList script over!"