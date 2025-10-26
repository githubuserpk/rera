FROM nginx:alpine

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Update nginx.conf to listen on port 8080
RUN sed -i 's/listen\s*80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# Create a directory for the mount point
RUN mkdir -p /etc/nginx/external-conf

# Use the external configuration file directly
CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/external-conf/nginx.conf"]

