FROM ubuntu:latest
LABEL authors="vadym"

ENTRYPOINT ["top", "-b"]