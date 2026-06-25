#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -qq && apt-get install -y -q curl

# Install uv
curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh

# Install the package
/root/.local/bin/uv sync

# Wrapper script so `terminus2` is on PATH
PROJECT_DIR=$(pwd)
cat > /usr/local/bin/terminus2 << WRAPPER
#!/bin/bash
exec "$PROJECT_DIR/.venv/bin/python" -m terminus2.cli "\$@"
WRAPPER
chmod +x /usr/local/bin/terminus2
