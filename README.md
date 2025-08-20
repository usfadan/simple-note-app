# Simple Notes App - Vulnerable vs Secure Source code Code

A Flask-based web application demonstrating vulnerable and secure implementations for SQL Injection and XSS, with a modern UI and note management functionality for educational purposes.

**WARNING**: This project is intentionally vulnerable for teaching purposes. Do NOT use in production or on a public server. Run it locally for training only.

## Overview

This project is a Flask web app designed to teach web security concepts by comparing vulnerable and secure implementations of a note-taking application. It includes:

- **Vulnerable Endpoints**: Demonstrate SQL Injection (via string concatenation) and XSS (via unescaped HTML) risks in add, delete, and search functionalities.
- **Secure Endpoints**: Use parameterized queries and HTML escaping to mitigate SQL Injection and XSS.
- **Enhanced UI**: A responsive, card-based interface with clear visual distinction between vulnerable (red) and secure (green) sections.
- **Docker and Kubernetes**: Includes vulnerable and secure Dockerfiles and Kubernetes configurations to demonstrate container security practices.

## Prerequisites

- Python 3.9+ (for local or vulnerable Docker) or 3.12+ (for secure Docker)
- Docker (optional, for containerized deployment)
- Kubernetes (optional, for orchestration)
- `curl` (for health checks in Docker/Kubernetes)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/vulnerable-notes-app.git
   cd vulnerable-notes-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Locally**:
   ```bash
   python app.py
   ```
   Access the app at `http://localhost:5000`.

## Docker Setup

- **Vulnerable Docker**:
  ```bash
  docker build -t vuln-flask-app -f Dockerfile.vulnerable .
  docker run -p 5000:5000 vuln-flask-app
  ```

- **Secure Docker**:
  ```bash
  docker build -t secure-flask-app -f Dockerfile.secure .
  docker run -p 5000:5000 secure-flask-app
  ```

## Kubernetes Setup

1. **Apply Configurations**:
   ```bash
   kubectl apply -f k8s-secret.yaml
   kubectl apply -f k8s-deployment.yaml
   kubectl apply -f k8s-networkpolicy.yaml
   ```

2. **Access the App**:
   ```bash
   kubectl port-forward svc/secure-app-service 5000:80
   ```
   Access at `http://localhost:5000`.

## Contributing

This is an educational project. Contributions to enhance demos or add new vulnerability examples are welcome. Please submit pull requests or open issues.

## License

This project is licensed under the MIT License. Use it for educational purposes only.

**Disclaimer**: This app is for learning about web security. Deploying it publicly may expose your system to attacks. Always test in a controlled, local environment.
