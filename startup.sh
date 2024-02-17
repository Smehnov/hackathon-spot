#!/bin/bash

ngrok tcp 22 > /dev/null &

export WEBHOOK_URL="$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")"

echo $WEBHOOK_URL

python3.8 main.py
