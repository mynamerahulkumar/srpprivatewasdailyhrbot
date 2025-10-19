#!/usr/bin/env python3
"""
Simple wrapper to run the bot with correct imports
"""
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

# Now import and run
from main import main

if __name__ == "__main__":
    main()

