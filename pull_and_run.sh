docker rm -f file_organizer
echo y | docker image prune -a
docker run -v .:/host-volume-bridge -it --rm --name file_organizer zadams104/file-organizer
docker exec -it file_organizer /bin/bash