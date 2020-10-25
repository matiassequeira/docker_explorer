<p align="center">
  <img src="https://github.com/matiassequeira/docker_explorer/blob/master/utils/docker_explorer_transparent_v6.jpg" />
</p>

# Docker Images Explorer

## Triage the data

In case you scanned a decent amount of images and obtained many findings, you might need to clean up and triage the data. For this, I've developed a few scripts which I recommend to take a look at first. To run the triage first you need to export this script to the path and execute it in the output path you selected:


1. Export script to PATH:

``` 
cd whispers/utils
export PATH=$PATH:$(pwd)
chmod +x classify_data.sh
```

2. Locate your output directory and run:

```
classify_data.sh
```


After this, you'll see a `./triaged` directory was created. Within this directory, there are two important files: `triaged_blocker.txt` and `triaged_critical.txt`.
