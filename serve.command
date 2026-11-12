#!/bin/bash
# Double-click this file to preview the Nibarc site locally.
cd "$(dirname "$0")/site" || { echo "Could not find the site/ folder."; read -n 1; exit 1; }
PORT=8787
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed. Install Xcode command line tools: xcode-select --install"
  read -n 1; exit 1
fi
echo "Nibarc  ->  http://localhost:$PORT/"
echo "Nexora  ->  http://localhost:$PORT/nexora/"
echo "Press Ctrl-C to stop."
( sleep 1; open "http://localhost:$PORT/" ) &
python3 -m http.server "$PORT"
