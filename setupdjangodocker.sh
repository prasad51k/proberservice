#!/bin/bash
set -e  # Exit the script on any error
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
