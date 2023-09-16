#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo -e "Usage: $0 filepath\n"
    exit 1
fi

filepath=$1

if [ ! -f "$filepath" ]; then
    echo -e "File $filepath not found!\n"
    exit 1
fi

task=$(grep -oP '"task":\s*"\K[^"]+' "$filepath")
task_graph=$(grep -oP '"task_graph":\s*"\K[^"]+' "$filepath")
python3 bazik.py $task --task-graph=$task_graph