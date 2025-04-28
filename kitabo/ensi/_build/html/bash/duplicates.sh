#!/bin/bash

# List all files and directories ending with ' 2'
duplicates=$(ls | grep ' 2$')

# Loop through each duplicate and remove it
for item in $duplicates; do
    echo "Removing $item"
    rm -rf "$item"
done

echo "Cleanup completed."
# flick 20250409213603-sGTG
# flick 20250409214209-0bRH
# flick 20250409214626-L6G1
# flick 20250409230551-0bKp
# flick 20250410002735-6njC
