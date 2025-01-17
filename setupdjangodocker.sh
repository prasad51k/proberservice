#!/bin/bash
# Update packages
echo "Setting up Django application..."
# Install necessary packages
sudo yum update -y
sudo yum install -y git curl docker amazon-ecr-credential-helper

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add EC2 user to Docker group to avoid sudo
sudo usermod -aG docker ec2-user
newgrp docker

# Clone your Django application repository
git clone https://github.com/prasad51k/proberservice.git /home/ec2-user/proberservice
cd /home/ec2-user/proberservice

# Build the Docker image
docker build -t proberservice1 .
docker run -d -p 8000:8000 proberservice1

# Push the Docker image to a Docker registry
# Replace <registry_url>, <username>, and <password> with appropriate Docker Hub or other registry credentials
REGISTRY_URL=" https://registry.hub.docker.com/durga51"  # e.g., for Docker Hub: docker.io/<username>
DOCKER_USERNAME="prasad.kedarisetti51@gmail.com"
DOCKER_PASSWORD="Durga@12345"

echo "$DOCKER_PASSWORD" | docker login $REGISTRY_URL -u "$DOCKER_USERNAME" --password-stdin
docker tag proberservice1:latest $REGISTRY_URL/proberservice1:latest
docker push $REGISTRY_URL/proberservice1:latest

echo "Django application Docker image pushed successfully."
