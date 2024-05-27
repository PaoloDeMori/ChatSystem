#!/bin/bash

# Verifica se python3 è installato
if command -v python3 &>/dev/null; then
    python3 ./client.py
else
    echo "Python3 non è installato"
fi




