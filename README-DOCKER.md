# Docker Run Guide

This guide explains how users can pull images and run the app directly in Docker Desktop.

## Method 1- Terminal Method (Fastest)

Docker images:

Backend- https://hub.docker.com/r/shivam18213/distance-calculator

Frontend- https://hub.docker.com/r/shivam18213/distance-calculator-frontend

```bash
docker login
docker pull shivam18213/distance-calculator-backend:latest
docker pull shivam18213/distance-calculator-frontend:latest

docker run -d --name distance-backend-run -p 5000:5000 shivam18213/distance-calculator-backend:latest
docker run -d --name distance-frontend-run -p 3000:3000 -e REACT_APP_API_URL=http://localhost:5000/api shivam18213/distance-calculator-frontend:latest
```

Open: `http://localhost:3000`

## Docker Desktop UI Method

1. Open Docker Desktop and go to **Images**.
2. Click **Pull**.
3. Enter backend image name: `shivam18213/distance-calculator-backend:latest` and pull.
4. Pull frontend image: `shivam18213/distance-calculator-frontend:latest`.
5. Click **Run** for backend image with:
   - Container name: `distance-backend-run`
   - Host port: `5000`
   - Container port: `5000`
6. Click **Run** for frontend image with:
   - Container name: `distance-frontend-run`
   - Host port: `3000`
   - Container port: `3000`
   - Environment variable: `REACT_APP_API_URL=http://localhost:5000/api`
7. Open `http://localhost:3000`.

```bash
docker rm -f distance-backend-run distance-frontend-run
```




## Method 2- Run With Docker Images

### Prerequisites

- Docker Desktop installed and running
- Terminal opened in the project root (`distance-calculator`)

### Build Images

Build backend image:

```bash
docker build -t distance-calculator-backend -f Dockerfile .
```

Build frontend image:

```bash
docker build -t distance-frontend -f frontend/Dockerfile ./frontend
```

### Run Containers

Run backend:

```bash
docker run -d --name distance-backend-run -p 5000:5000 distance-calculator-backend
```

Run frontend:

```bash
docker run -d --name distance-frontend-run -p 3000:3000 -e REACT_APP_API_URL=http://localhost:5000/api distance-frontend
```

### Access URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api

### Manage Containers

List running containers:

```bash
docker ps
```

View logs:

```bash
docker logs -f distance-backend-run
docker logs -f distance-frontend-run
```

Stop containers:

```bash
docker stop distance-backend-run distance-frontend-run
```

Remove containers:

```bash
docker rm distance-backend-run distance-frontend-run
```

If names already exist, recreate:

```bash
docker rm -f distance-backend-run distance-frontend-run
docker run -d --name distance-backend-run -p 5000:5000 distance-calculator-backend
docker run -d --name distance-frontend-run -p 3000:3000 -e REACT_APP_API_URL=http://localhost:5000/api distance-frontend
```

### Optional: Docker Compose

```bash
docker compose up --build -d
```

Stop compose services:

```bash
docker compose down
```
