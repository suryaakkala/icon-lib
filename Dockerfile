# Use nginx to serve static content
FROM nginx:alpine

# Remove default nginx config
RUN rm -rf /usr/share/nginx/html/*

# Copy everything from src/ into nginx's static folder
COPY src/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80
