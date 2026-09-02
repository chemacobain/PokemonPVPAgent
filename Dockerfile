# Build stage for Vue.js Frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
# Copy package.json and install dependencies
COPY frontend/package*.json ./
RUN npm install
# Copy the rest of the frontend source and build
COPY frontend/ ./
ARG VITE_GA_ID
ENV VITE_GA_ID=$VITE_GA_ID
RUN npm run build

# Production stage for Python Flask Backend
FROM python:3.9-slim
WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY *.py ./
COPY assets/ ./assets/

# Copy built frontend from the previous stage
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Expose the port the app runs on
EXPOSE 8080

# Configure environment variables
ENV PORT=8080
ENV FLASK_ENV=production

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "server:app"]
