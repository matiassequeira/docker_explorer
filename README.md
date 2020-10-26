<p align="center">
  <img src="https://github.com/matiassequeira/docker_explorer/blob/master/utils/docker_explorer_transparent_v6.jpg" />
</p>

# Docker Images Explorer

This tool scans (for the moment) Dockerhub images that match a given keyword in order to find "forgotten" secrets. The scan engine used is a modified fork from [Whispers](https://github.com/Skyscanner/whispers).

Using the tool, I found numerous AWS credentials, SSH private keys, databases, API keys, etc. It’s an interesting tool to add to the bug hunter / pentester arsenal, not only for the possibility of finding secrets, but for fingerprinting an organization. If you are a DevOps or Security Engineer, you might want to integrate the scan engine to your CI/CD for your Docker images.

## Prerequisites: 

* Python3
* Pip3
* Docker


## Installation (tested in Ubuntu and macOS)

Since the execution of this tool can take a long time and it's very CPU demanding, it's recommended to run it in a VPS running Ubuntu (I'm working on a Terraform template to ease the setup). To prepare the environment for Docker Explorer (install whispers and Python requirements), run the following commands:

```
git clone https://www.github.com/matiassequeira/docker_explorer
cd docker_explorer
chmod +x install.sh
export PATH=$(pwd):$PATH
./install.sh
```

## Usage

It's recommended to run this tool in a fresh new directory in order to keep the tool separate from the output. Momentarily, there are two scripts you can execute according to your needs:

### ExploreAll

```
❯ ./ExploreAll -h
usage: ExploreAll [-h] -t TARGET [-c CONFIG] [-o OUTPUT] [--tmp TMP] [--page_size PAGE_SIZE] [--timeout TIMEOUT]
                  [--order-by-pull-count [{ASC,DESC}]] [-p PROCESSES] [--start START] [--end END]

Docker Images Scanner. This script receives a keyword and it starts to scan all matching DockerHub images.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Whispers custom config filepath. By default will use Docker Explorer whispers config.
  -o OUTPUT, --output OUTPUT
                        Directory where to store matching files. Will use ./ by default.
  --tmp TMP             Temporary path to dump the filesystem and perform the scan. Default is /tmp
  --page_size PAGE_SIZE
                        Size of the Dockerhub API page. Default 100.
  --timeout TIMEOUT     Timeout in minutes for scan engine execution per image. Default 45 minutes.
  --order-by-pull-count [{ASC,DESC}]
                        Order by the amount of pull counts of the image. The lesser pulls, the newer the image.
  -p PROCESSES, --processes PROCESSES
                        Amount of parallel processes. Default is 4
  --start START         Start page
  --end END             End page

Required arguments:
  -t TARGET, --target TARGET
                        Keyword to search in dockerhub
```

An example of this command that scans all the images matching the keyword **aws** is:

```
./ExploreAll -t aws
```

If you're using a VPS with Ubuntu, I recommend to leave it running in background with the `nohup` (no hangup) command and redirect the logs to a file that you can `cat` to track progress:

```
nohup ExploreAll -t aws &> out.txt &
tail -f out.txt
```

### ExploreImage

```
❯ ./ExploreImage -h
usage: ExploreImage [-h] [-i IMAGE] [-f FILE] [-o OUTPUT] [-c CONFIG] [--tmp TMP] [--timeout TIMEOUT] [-p PROCESSES]

Scan a single image or a given list of DockerHub images

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Image to scan in dockerhub. It will be used the latest version by default. The format is
                        repository/image_name:tag.
  -f FILE, --file FILE  File with list of images to scan in the format repository/image_name:tag.
  -o OUTPUT, --output OUTPUT
                        Directory where to store matching files. Will use ./ by default.
  -c CONFIG, --config CONFIG
                        Whispers custom config filepath. By default will use Docker Explorer whispers config.
  --tmp TMP             Temporary path to dump the filesystem and perform the scan. Default is /tmp
  --timeout TIMEOUT     Timeout in minutes for scan engine execution per image. Default 45 minutes.
  -p PROCESSES, --processes PROCESSES
                        Amount of parallel processes. Default is 4.
```

An example of this command to scan a specific image is:

```
./ExploreImage -i repository/image_name:image_tag 
```

## Data triage

In case you scanned a decent amount of images and obtained many findings, you might need to triage the data. For this, I've developed a few scripts which I recommend to take a look at first. 

To run the triage you need to locate your output directory and run:

```
cd YOUR_docker_explorer_output
classify_data.sh
```

After this, you'll see that a `./triaged` directory was created. Within this directory, there are two important files: `triaged_blocker.txt` and `triaged_critical.txt`, as well as the potential files with secrets separated in folders.

## Finished? Cleanup your disk!

If you're done scanning your Docker images and **saved your results**, you might need to delete some files / directories / containers / images, for which I have a script with a few commands that I **recommend to check first**. The cleanup script should be run in the directory where it's stored the output of your scan. After this, your containers, images, and files in the current directory will re removed:

```
cleanup.sh
```

## TODO
* Integrate with quay.io
* Add functionality to explore older version of an image
* Add plugin to whispers: Run string command on binaries and report strings that meet certain entropy and extra conditions.
