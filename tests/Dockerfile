FROM ubuntu:20.04
RUN apt update && apt install curl -y
WORKDIR /src
COPY . .
RUN chmod +x ./tests.sh
CMD ["bash", "tests.sh"]
