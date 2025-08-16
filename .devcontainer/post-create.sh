#!/usr/bin/env bash

if ! command -v uv &>/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

uv venv .venv

uv pip install -r pyproject.toml

if ! grep -q "source .venv/bin/activate" ~/.zshrc; then
  echo 'source .venv/bin/activate' >> ~/.zshrc
fi
