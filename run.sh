#!/usr/bin/env bash
echo ""
echo "compile the Data"
echo ""

rm -r compiled_data/
mkdir compiled_data
cd script
python3.5 ./compile_data.py



