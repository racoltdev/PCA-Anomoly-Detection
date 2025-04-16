#! /usr/bin/bash
mkdir ./cap
sudo chown -R root:root ./cap
sudo tshark -w ./cap/output.pcapng -b duration:3600 -a duration:172800
