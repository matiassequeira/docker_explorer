find . -name "*.log" -type f -maxdepth 1 -exec cat {} + | grep "CRITICAL" >> critical.txt
find . -name "*.log" -type f -maxdepth 1 -exec cat {} + | grep "BLOCKER" >> blocker.txt
chmod +x TriageBlockerAndCritical
sudo TriageBlockerAndCritical
touch to_see.txt
sudo chown -R "$(whoami)" triaged