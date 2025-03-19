# # Step 1: Build Angular App
# FROM node:18 AS build
# WORKDIR /app
# COPY package.json package-lock.json ./
# RUN npm install
# COPY . .
# RUN npm run build --configuration=production

# # Step 2: Use Nginx to Serve Angular
# FROM nginx:alpine
# WORKDIR /usr/share/nginx/html

# # Copy built Angular files
# COPY --from=build /app/dist/frontend .

# # Copy the custom Nginx config
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Expose port 80
# EXPOSE 80

# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]
# Step 1: Build Angular App
# Step 1: Build Angular App
FROM node:18 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build --configuration=production

# Step 2: Serve with http-server
FROM node:18
WORKDIR /usr/src/app
RUN npm install -g http-server  # Install http-server globally

# Copy built Angular files from the previous stage
COPY --from=build /app/dist/frontend .

# Expose port 80
EXPOSE 80

# Start the http-server and serve files from the current directory
CMD ["http-server", "-p", "80", "."]

