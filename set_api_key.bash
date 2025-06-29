#!/bin/bash

# Display a warning that the script is for Linux only
echo "Warning: This script will only work on Linux systems."

# Check if the system is Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "This script is only supported on Linux. Exiting."
    exit 1
fi

# Ask for the API key
read -p "Enter your Gemini API Key: " API_KEY

# Check if the API key is empty
if [ -z "$API_KEY" ]; then
    echo "API key cannot be empty. Exiting."
    exit 1
fi

# Add the API key to the environment variables temporarily (for the current session)
export GEMINI_API_KEY="$API_KEY"

# Add the API key permanently by appending to .bashrc (or .bash_profile or .zshrc depending on shell)
echo "export GEMINI_API_KEY=\"$API_KEY\"" >> ~/.bashrc

# Source the .bashrc to apply changes immediately
source ~/.bashrc

echo "API key has been added successfully and is available for the current session."