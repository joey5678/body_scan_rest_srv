#!/bin/sh
# run in dev mode

docker run -it --rm --name ft_rest_srv -p 8100:80 --link redis-outer:redis-outer -v `pwd`/:/app/ ft_rest_server_image

