FROM nginx:alpine

# Remove default nginx config
RUN rm -rf /usr/share/nginx/html/*

# Copy your static site into nginx's web root
COPY src/ /usr/share/nginx/html/

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
