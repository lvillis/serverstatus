# build stage
FROM node:lts-alpine AS build-stage
WORKDIR /app
COPY dashboard/package*.json ./
RUN npm install
COPY dashboard/ .
RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

# https://unix.stackexchange.com/questions/36795/find-sed-search-and-replace
# https://www.thinbug.com/q/40449605
CMD  find /usr/share/nginx/html/js -name "index.*.js" -exec sed -i'' -e "s,http://127.0.0.1:20000/get,$API_URL,g" {} + && nginx -g "daemon off;"
