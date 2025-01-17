#!/bin/bash
set -e  # Exit the script on any error

# Update packages
echo "Setting up Django application..."
sudo yum update -y
sudo yum install -y git
sudo yum install -y docker
# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add EC2 user to Docker group
sudo usermod -aG docker ec2-user
# Commenting out 'newgrp docker' to avoid script termination
# Logout and log back in for changes to take effect

# Clone your Django application repository
if [ ! -d "/home/ec2-user/proberservice" ]; then
  git clone https://github.com/prasad51k/proberservice.git /home/ec2-user/proberservice
else
  echo "Repository already exists. Pulling latest changes..."
  cd /home/ec2-user/proberservice
  git pull
fi
cd /home/ec2-user/proberservice

# Build the Docker image
docker build -t proberservice1 .

# Run the Docker container
docker run -d -p 8000:8000 proberservice1

# Push the Docker image to a Docker registry
DOCKER_USERNAME="prasad.kedarisetti51@gmail.com"
DOCKER_PASSWORD="Durga@12345"
IMAGE_NAME="durga51/proberservice1"  # Replace 'durga51' with your Docker Hub username or namespace
TAG="latest"

# Docker login
echo "$DOCKER_PASSWORD" | docker login docker.io -u "$DOCKER_USERNAME" --password-stdin

# Tag the Docker image with the proper repository name
docker tag proberservice1:latest docker.io/$IMAGE_NAME:$TAG

# Push the Docker image
docker push docker.io/$IMAGE_NAME:$TAG

echo "Django application Docker image pushed successfully."
