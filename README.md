<p align="center">
  <img src="https://github.com/matiassequeira/docker_explorer/blob/master/utils/docker_explorer_transparent_v6.jpg" />
</p>

# Docker Images Explorer

This tool intends to scan (for the moment) Dockerhub images that match a given keyword in order to find secrets. The scan engine used is a fork from [Whispers](https://github.com/Skyscanner/whispers).


## Installation
To prepare the environment for DockeExplore (install whispers and Python requirements), run the following commands:

```
git clone https://www.github.com/matiassequeira/docker_explorer
cd docker_explorer
chmod +x install.sh
./install.sh
```

## Usage



## TODO
* Integrate with quay.io
* Add functionality to explore older version of an image
* Add plugin to whispers: Run string command on binaries and report strings that meet certain entropy and extra conditions.
