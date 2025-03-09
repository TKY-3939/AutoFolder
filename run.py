#!/usr/bin/env python3
"""
Simple script to run the AutoFolder application.
"""

import sys
from app import app

if __name__ == "__main__":
    try:
        port = 8765
        print(f"Starting AutoFolder web interface on http://127.0.0.1:{port}")
        print("Press Ctrl+C to stop the server")
        app.run(debug=False, port=port)
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0) 