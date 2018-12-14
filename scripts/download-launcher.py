#!/usr/bin/env python3

import os.path
from urllib.request import urlretrieve 


def main():
    urlretrieve("https://s3.amazonaws.com/Minecraft.Download/launcher/Minecraft.jar", "Minecraft.jar")
main()
