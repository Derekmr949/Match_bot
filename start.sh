#!/usr/bin/env bash
# Lance un mini serveur web en arrière-plan pour satisfaire Render
python3 -m http.server 10000 &
# Lance ton bot Telegram
python3 bot.py
