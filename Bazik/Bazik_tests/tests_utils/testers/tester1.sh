#!/bin/bash



file1=$1
file2=$2


if [ ! -f "$file1" ]; then
    echo "File $file1 not found!"
    exit 1
fi

if [ ! -f "$file2" ]; then
    echo "File $file2 not found!"
    exit 1
fi


if diff -q "$file1" "$file2" > /dev/null; then
    echo -e "Remove comments test passed\n"
    echo "passed" > "../Bazik_tests/test_results/test9_result.txt"
else
    echo -e "Remove comments test failed\n"
    echo "failed" > "../Bazik_tests/test_results/test9_result.txt"
fi
