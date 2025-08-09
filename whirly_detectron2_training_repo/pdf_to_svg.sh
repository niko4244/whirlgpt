#!/bin/bash
# Script to convert PDF pages to SVG using pdf2svg

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input.pdf output_prefix"
    exit 1
fi

INPUT_PDF=$1
OUTPUT_PREFIX=$2

pdf2svg "$INPUT_PDF" "${OUTPUT_PREFIX}_page_%d.svg" all
