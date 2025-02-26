docker rm -f file-organizer
echo y | docker image prune -a
docker build -t file-organizer .
docker run -v .:/host-volume-bridge -it --rm --name file-organizer file-organizer
docker exec -it file-organizer /bin/bash