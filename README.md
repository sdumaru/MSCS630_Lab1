# Multithreaded Word-Frequency Counter

## Overview
Reads a text file, splits it into N segments, processes each segment concurrently with threads, and consolidates intermediate counts into a final word-frequency table.

## Requirements
- Python 3.7+
- No external libraries

## Usage
```bash
python main.py <path/to/textfile> <num_segments>
