#!/bin/bash
# Script para iniciar BlackBoxK asegurando DISPLAY

if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

source venv/bin/activate
python3 main.py
