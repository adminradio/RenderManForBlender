@echo off
docker run --rm -it -v "%cd%":/docs squidfunk/mkdocs-material build
