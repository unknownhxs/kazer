#!/usr/bin/env python3
"""
KASER File Manager Launcher
Easy way to run the file manager from the tools directory
"""

import sys
import os
from pathlib import Path

# Add the file manager directory to Python path
sys.path.append('file manager')

try:
    from file_manager import FileManager
    
    def main():
        """Main function to start the file manager"""
        print("🚀 Starting KASER File Manager...")
        
        # Create and start the file manager
        fm = FileManager()
        fm.load_language_settings()
        
        print(f"🌍 Language: {fm.current_language}")
        print("📁 Starting file manager...")
        
        # Start the main loop
        fm.run()
        
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error importing file manager: {e}")
    print("Make sure you're running this from the tools directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting file manager: {e}")
    sys.exit(1)
