#!/bin/bash

echo "#________      _____                     _____             ____  __#
#____  */*_______  /___________  ___________(_)______________  |/ /#
# **  / **  ** \  **/_  ___/  / / /_  ___/_  /_  __ \_  __ \_    / #
#__/ /  *  / / / /* *  /   / /*/ /_(__  )_  / / /_/ /  / / /    |  #
#/___/  /_/ /_/\__/ /_/    \__,_/ /____/ /_/  \____//_/ /_//_/|_|  #

This is for setup                          Insta:intrusionx_offical
####################################################################"

echo "Updating system and installing dependencies..."
sudo apt update -y
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    python3-dev \
    build-essential \
    curl \
    unzip \
    wget \
    gcc \
    g++ \
    make \
    golang


echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Install gf using modern Go install command
echo "Installing gf using Go..."
# Set up Go environment variables explicitly
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Create Go directories if they don't exist
mkdir -p $GOPATH/bin

# Install gf using go install (modern approach)
echo "Installing gf using modern Go command..."
go install github.com/tomnomnom/gf@latest

# Check if installation was successful
if [ -f "$GOPATH/bin/gf" ]; then
    echo "gf successfully installed at $GOPATH/bin/gf"
else
    echo "Warning: gf installation might have failed. Trying direct download as fallback..."
    # Fallback to direct binary download if Go install fails
    mkdir -p ~/.local/bin
    curl -Lo ~/.local/bin/gf https://github.com/tomnomnom/gf/releases/latest/download/gf-linux-amd64
    chmod +x ~/.local/bin/gf
    echo "export PATH=\$PATH:~/.local/bin" >> ~/.bashrc
fi

# Create ~/.gf directory for pattern files
echo "Setting up gf pattern files..."
mkdir -p ~/.gf

# Clone the repository temporarily to get the example patterns and completion script
echo "Getting gf patterns and completion script..."
TEMP_DIR=$(mktemp -d)
git clone https://github.com/tomnomnom/gf.git "$TEMP_DIR"

# Copy example patterns
if [ -d "$TEMP_DIR/examples" ]; then
    cp -r "$TEMP_DIR/examples/"* ~/.gf/
    echo "Copied default gf patterns to ~/.gf/"
else
    echo "Warning: Could not find gf examples directory"
fi

# Set up completion
if [ -f "$TEMP_DIR/gf-completion.bash" ]; then
    # Save completion script to a permanent location
    mkdir -p ~/.local/share/gf
    cp "$TEMP_DIR/gf-completion.bash" ~/.local/share/gf/
    
    # Add to bashrc if not already there
    if ! grep -q "gf-completion.bash" ~/.bashrc; then
        echo "source ~/.local/share/gf/gf-completion.bash" >> ~/.bashrc
        echo "Added gf-completion to ~/.bashrc"
    fi
else
    echo "Warning: Could not find gf-completion.bash"
fi

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Check if the Gf-Patterns directory already exists
if [ ! -d "Gf-Patterns" ]; then
    # Clone the Gf-Patterns repository if it doesn't exist
    echo "Cloning Gf-Patterns repository..."
    git clone https://github.com/1ndianl33t/Gf-Patterns.git
    
    # Copy custom patterns to ~/.gf
    if [ -d "Gf-Patterns" ]; then
        cp Gf-Patterns/*.json ~/.gf/
        echo "Copied custom patterns to ~/.gf/"
    fi
else
    echo "Gf-Patterns directory already exists, skipping clone."
    # Make sure patterns are copied
    cp Gf-Patterns/*.json ~/.gf/ 2>/dev/null || echo "No patterns to copy from Gf-Patterns"
fi

# Update PATH in bashrc if not already there
if ! grep -q "GOPATH=.*go" ~/.bashrc; then
    echo "export GOPATH=\$HOME/go" >> ~/.bashrc
fi

if ! grep -q "PATH=.*GOPATH/bin" ~/.bashrc; then
    echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.bashrc
fi

# Notify the user that the installation is complete
echo "Installation complete! You can now use the 'gf' tool and the Python dependencies."

# Deactivate the virtual environment
deactivate

echo "Please run 'source ~/.bashrc' to apply changes or restart your terminal"
