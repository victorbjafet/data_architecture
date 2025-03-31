#!/bin/bash

for i in {1..4}; do
    node="node$i"
    if ping -c 1 -W 1 "$node" &> /dev/null; then
        echo "$node is UP"
    else
        echo "$node is DOWN"
    fi
done
