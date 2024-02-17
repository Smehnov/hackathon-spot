#!/bin/bash

ngrok config add-authtoken 4K4LMsW25XZAjYQJDjoyF_rcg3gYWP48R8J2AmFELL

nohup ngrok tcp 22 > /dev/null &

python3.8 wait.py

export WEBHOOK_URL="$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")"

echo $WEBHOOK_URL

curl -X POST https://webhook.site/5d7666da-f292-4cc6-b55e-dbd60c35c2d6 -d "url=${WEBHOOK_URL}"

python3.8 main.py
