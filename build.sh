#!/bin/sh
# run in dev mode

docker build --no-cache --build-arg BUILDMODE=debug-docker -t ft_rest_server_image .

