# Raspberry Setup

## Hardare
Model: Raspberry Pi 4 Model B 1.4

Ethernet wire

## Software

OS: Raspian GNU/Linux 11

Python version: 3.9.2

## Configuration

This raspberry rebots every sunday at 00:00
this is achivied by running this commands

```
crontab -e
```

after you will be asked to select an editor, then put this line at the end of the opened file

```
0 0 * * 0 sudo reboot
```

to verify the changes, run the following cmd

```
crontab -l
```

