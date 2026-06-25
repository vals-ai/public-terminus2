#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -qq && apt-get install -y -q curl git openssh-client

# Install uv
curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh

# Configure SSH key for private repo access
mkdir -p /root/.ssh
echo "$MODEL_PROXY_SSH_KEY" > /root/.ssh/id_ed25519
chmod 600 /root/.ssh/id_ed25519
printf "Host github.com\n  StrictHostKeyChecking accept-new\n" > /root/.ssh/config
chmod 600 /root/.ssh/config

# Install the package
/root/.local/bin/uv sync --upgrade-package model-library

# Wrapper script so `terminus2` is on PATH
cat > /usr/local/bin/terminus2 << 'WRAPPER'
#!/bin/bash
exec /bundle/terminus2/.venv/bin/python -m terminus2.cli "$@"
WRAPPER
chmod +x /usr/local/bin/terminus2
