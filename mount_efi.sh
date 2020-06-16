#!/bin/sh

#This script is a simple way to remember how to mount EFI partition on mac
echo 'Run the following cmds'
echo 'diskutil list'
echo 'sudo mkdir /Volumes/EFI'
echo 'sudo mount -t msdos /dev/disk0s1 /Volumes/EFI'
