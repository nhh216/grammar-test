# Stage 1: Build Vue app
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
# Debug: check what was installed
RUN echo "=== node_modules/.bin ===" && ls node_modules/.bin/ | head -30
RUN echo "=== vite ===" && ls -la node_modules/.bin/vite || echo "VITE NOT FOUND"
RUN echo "=== vue-tsc ===" && ls -la node_modules/.bin/vue-tsc || echo "VUE-TSC NOT FOUND"
RUN echo "=== NODE_ENV ===" && echo $NODE_ENV
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
