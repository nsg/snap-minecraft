
prime: clean
	snapcraft

local: prime
	snap install --force-dangerous minecraft*.snap

clean:
	snapcraft clean
