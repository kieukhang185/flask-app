#!/bin/bash
genera_secret(){
    python3 -c "import secrets
    secrets.token_hex(32)"
}

change_docker_permission(){
    sudo chmod 666 /var/run/docker.sock
    ls -l /var/run/docker.sock
}

install_depen_all(){
    sudo apt update && sudo apt-get install -y git curl vim ca-certificates
    # Add Docker's official GPG key:
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    change_docker_permission
}

## docker compose build --no-cache web
## docker compose --env-file .env up
    