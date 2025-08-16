#!/usr/bin/env bash

export PATH="$HOME/.local/bin:$PATH"

# Create a virtual environment if it doesn't exist
[ -d .venv ] || uv venv .venv

# Activate the virtual environment
if ! grep -q "source .venv/bin/activate" ~/.zshrc; then
  echo 'source .venv/bin/activate' >> ~/.zshrc
fi

# Install dependencies
uv sync --all-extras
