#!/usr/bin/env python

from distutils.core import setup, Extension

setup(	name="spi",
	version="1.1",
	description="Python bindings for Linux SPI access through spi-dev",
	author="Volker Thoms",
	author_email="unconnected@gmx.de",
	maintainer="Volker Thoms",
	maintainer_email="unconnected@gmx.de",
	license="GPLv2",
	url="http://www.hs-augsburg.de/~vthoms",
	include_dirs=["/usr/include"],
	ext_modules=[Extension("spi", ["spimodule.c"])])
