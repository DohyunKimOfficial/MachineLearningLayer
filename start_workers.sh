#/bin/sh

# Starts 5 workers in parallel
python worker.py &
python worker.py &
python worker.py &
python worker.py &
python worker.py &
wait
