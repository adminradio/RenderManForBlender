#!/bin/sh
docker run --rm -it -p 8000:8000 -v `pwd`:/docs squidfunk/mkdocs-material
