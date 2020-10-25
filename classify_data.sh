find . -maxdepth 1 -name "*.log" -type f -exec cat {} + | grep "CRITICAL" >> critical.txt
find . -maxdepth 1 -name "*.log" -type f -exec cat {} + | grep "BLOCKER" >> blocker.txt
$(dirname $0)/utils/TriageBlockerAndCritical.py
sudo chown -R "$(whoami)" triaged