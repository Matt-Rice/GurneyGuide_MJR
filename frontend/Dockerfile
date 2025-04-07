### STAGE 1: BUILD ###
FROM node:18 AS build
WORKDIR /app

# Copy package files and install
COPY package*.json .
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the production version
RUN npm run build --prod

### STAGE 2: RUN ###
FROM nginx:latest

# Copy compiled Angular dist folder to Nginx html
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Copy your custom Nginx config into place
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
