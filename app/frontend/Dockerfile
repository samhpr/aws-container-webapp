FROM nginx:alpine

# Copy the static HTML file
COPY index.html /usr/share/nginx/html/

# Copy custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 3000
EXPOSE 3000

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
