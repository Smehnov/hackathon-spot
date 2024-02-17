FROM ghcr.io/merklebot/hackathon-arm-image:master as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

ARG Version
ARG GitCommit
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" 

RUN apt install curl

RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | tee /etc/apt/sources.list.d/ngrok.list && apt update -y && apt install ngrok -y

COPY --chmod=765 ./startup.sh .

COPY requirements.txt requirements.txt
RUN python3.8 -m pip install -r requirements.txt
COPY . .

CMD ["sh ./startup.sh"]
