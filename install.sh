#!/bin/bash

echo "Criando ambiente Hotmart"
python -m venv hotmart_venv

echo "Installing required Python packages..."
python -m pip install -r requirements.txt