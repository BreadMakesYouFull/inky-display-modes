#!/usr/bin/env bash
# Run
# Can be ran from raspi startup via rc-local / systemd / cron etc
bash -c "source ./venv/bin/activate; env INKY_IMG_DIR=${INKY_IMG_DIR:-./img/} python -m inkyfuncmap"
