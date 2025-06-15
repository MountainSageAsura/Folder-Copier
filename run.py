#!/usr/bin/env python3
"""
Simple run script for Enhanced Folder Copier
This ensures proper imports and paths are set up
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import and run main
if __name__ == "__main__":
    from main import main
    main()