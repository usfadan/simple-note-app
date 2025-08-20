# WARNING: This Dockerfile is intentionally vulnerable for educational purposes.
# Do NOT use in production.

# Using root user (VULNERABLE: Runs container with excessive privileges)
FROM python:3.9

# Exposing unnecessary ports (VULNERABLE: Exposes more than needed)
EXPOSE 5000 22 80 443

# Copying sensitive files unnecessarily (VULNERABLE: Could expose secrets)
COPY . /app
WORKDIR /app

# Installing all dependencies without verification (VULNERABLE: No version pinning)
RUN pip install flask

# Running as root (VULNERABLE: Should use a non-root user)
CMD ["python", "app.py"]
