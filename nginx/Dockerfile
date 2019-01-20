# Set nginx base image
FROM nginx:stable-alpine

# Copy custom configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod 777 -R /usr/share/nginx/
RUN chown -R nginx:nginx /usr/share/nginx/

CMD ["nginx", "-g", "daemon off;"]