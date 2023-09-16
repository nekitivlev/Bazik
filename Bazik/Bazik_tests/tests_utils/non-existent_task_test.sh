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
python3 bazik.py $task --task-graph=$task_graph 2> "../Bazik_tests/outputs/non-existent_task_out.txt"

# Find the line number where "Traceback" starts
traceback_line=$(grep -n 'Traceback' "../Bazik_tests/outputs/non-existent_task_out.txt" | cut -d : -f 1)

# If "Traceback" line is found, delete lines from "Traceback" to the penultimate line, keeping the last line
if [ ! -z "$traceback_line" ]; then
    total_lines=$(wc -l < "../Bazik_tests/outputs/non-existent_task_out.txt")
    let "end_line = total_lines - 1"
    sed -i "${traceback_line},${end_line}d" "../Bazik_tests/outputs/non-existent_task_out.txt"
fi