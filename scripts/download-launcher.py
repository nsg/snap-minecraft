#!/usr/bin/env python3

import os.path
from urllib.request import urlretrieve 
import subprocess
import os
import re


def main():
    urlretrieve("https://launcher.mojang.com/download/Minecraft.tar.gz", "minecraft-launcher.tar.gz")
    
    subprocess.call(['tar','-xzf','minecraft-launcher.tar.gz'])
    
    subprocess.call(['rm','-rf','minecraft-launcher.tar.gz'])
    
main()

