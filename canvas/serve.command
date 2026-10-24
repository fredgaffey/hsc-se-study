#!/bin/bash
cd "$(dirname "$0")"
echo "SEN Offline running at http://localhost:8765"
echo "Open that in Chrome, then use the Install button (or the icon in the address bar)."
echo "Press Ctrl-C to stop."
python3 -m http.server 8765
