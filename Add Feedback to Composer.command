#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Python script
cd "$SCRIPT_DIR"
python "$SCRIPT_DIR/add_feedback_to_composer.py"

# Keep the terminal window open for a moment to see the output
sleep 3 