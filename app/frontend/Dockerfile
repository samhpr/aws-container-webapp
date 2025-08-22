FROM nginx:alpine

# copy the static HTML file
COPY index.html /usr/share/nginx/html/

# copy custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# expose port 3000
EXPOSE 3000

# run nginx for this example
CMD ["nginx", "-g", "daemon off;"]
