#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from urllib.request import urlretrieve
from threading import Thread
import hashlib
import os.path
import subprocess

DOWNLOAD_LINK = "http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz"
DOWNLOAD_COOKIE = "gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie"
DOWNLOAD_SHA256 = "c78200ce409367b296ec39be4427f020e2c585470c4eed01021feada576f027f"
DOWNLOAD_FILE = "jdk-8u151-linux-x64.tar.gz"

class SnapUIWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Java Downloader")
        self.set_border_width(10)
        self.set_default_size(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Snap Java Downloader"
        self.set_titlebar(hb)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        label = Gtk.Label("This tool will download Oracle JDK to your computer.")
        label.set_line_wrap(True)
        vbox.pack_start(label, False, True, 10)

        label = Gtk.Label("This is an unofficial Minecraft snap. For legal reasons "
                          "I can't distribute Java directly in the snap "
                          "so this tool will download it for you.\n\n"
                          "Do you agree to the license at: "
                          "http://www.oracle.com/technetwork/java/javase/terms/license/index.html")

        label.set_line_wrap(True)
        vbox.pack_start(label, False, True, 10)

        button1 = Gtk.LinkButton("http://www.oracle.com/technetwork/java/javase/downloads/index.html", "Read more about Java")
        vbox.pack_start(button1, False, True, 0)
        button1 = Gtk.LinkButton("http://www.oracle.com/technetwork/java/javase/terms/license/index.html", "Java License")
        vbox.pack_start(button1, False, True, 0)
        button2 = Gtk.LinkButton("https://github.com/nsg/snap-minecraft", "Submit an issue or PR")
        vbox.pack_start(button2, False, True, 0)

        button = Gtk.Button.new_with_mnemonic("Download and agree to the License")
        button.connect("clicked", self.on_clicked)
        vbox.pack_start(button, False, True, 40)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 20)

    def on_clicked(self, button):
        self.message("Downloading Oracle Java")
        self.progressbar.set_show_text(True)
        button.hide()
        thread = Thread(target=self.download_thread)
        thread.start()

    def download_thread(self):
        # I would love a PR/feedback how to download this send the cookie
        # and still have the report hook feature for the progressbar
        # (see the launcher downloader).

        cmd = [
            "wget",
            "--no-cookies",
            "--no-check-certificate",
            "--header",
            "Cookie: {}".format(DOWNLOAD_COOKIE),
            DOWNLOAD_LINK
            ]

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

        dh = hashlib.sha256(open(DOWNLOAD_FILE, 'rb').read()).hexdigest()
        if dh == DOWNLOAD_SHA256:
            self.message("Checksum matches")
            Gtk.main_quit()
        else:
            self.message("Error: Checksum {} did not match {}".format(dh, DOWNLOAD_SHA256))

    def reporthook(self, blocknum, blocksize, totalsize):
        p = round((blocknum * blocksize) / totalsize, 2)
        self.progressbar.set_fraction(p)

    def message(self, text):
        self.progressbar.set_text(text)
        print(text)

if not os.path.isfile(DOWNLOAD_FILE):
    win = SnapUIWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
