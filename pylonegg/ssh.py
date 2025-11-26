import os
import subprocess
from pathlib import Path

# Define ~/.ssh directory
ssh_dir = Path.home() / ".ssh"

# Create ~/.ssh directory if it doesn't exist
ssh_dir.mkdir(parents=True, exist_ok=True)

# Set key paths
key_path = ssh_dir / "id_rsa"

# Passphrase
passphrase = "SilverCanyon!Drift92"

# Build ssh-keygen command
cmd = [
    "ssh-keygen",
    "-t", "rsa",
    "-b", "2048",        # change to 4096 if preferred
    "-m", "PEM",
    "-f", str(key_path),
    "-N", passphrase
]

# Run the command
subprocess.run(cmd, check=True)

# Display results
print(f"Private key:  {key_path}")
print(f"Public key:   {key_path}.pub")
