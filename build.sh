#!/bin/sh
# run in dev mode

docker build --no-cache --build-arg BUILDMODE=debug-docker -t restpie-dev-image .

