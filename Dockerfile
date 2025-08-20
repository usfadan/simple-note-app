# This Dockerfile follows best security practices: minimal base image, non-root user, version pinning, minimal exposure, robust healthcheck.

# Use a slim base image to reduce attack surface
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with chown to non-root user
COPY --chown=appuser:appgroup . .

# Expose only the necessary ports (5000 for backend, 7860 for Gradio)
EXPOSE 5000 7860

# Robust healthcheck (SECURE: Checks app health with retries and timeout)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000 || exit 1

# Switch to non-root user
USER appuser

# Run the backend (Gradio runs separately or in another container)
CMD ["python", "app.py"]
