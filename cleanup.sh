docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q) -f
sudo rm -rf /tmp/explore_*
sudo rm -rf explore_* triaged/ logs/
rm *.zip out.txt whispers.log blocker.txt critical.txt