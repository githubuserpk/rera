FROM nginx:alpine

# Copy a custom nginx configuration if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Update nginx.conf to listen on port 8080
RUN sed -i 's/listen\s*80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]