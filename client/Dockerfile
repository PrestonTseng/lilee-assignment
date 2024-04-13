FROM node:lts-slim as build-stage
WORKDIR /app
ARG API_BASE_URL

COPY . .
RUN echo "NG_APP_API_BASE_URL=$API_BASE_URL" > .env

RUN npm install
RUN npm run build:prd

FROM node:alpine as production-stage
COPY --from=build-stage --chmod=777 /app/dist/client/browser /app/dist

ENV PORT=80
EXPOSE 80
ENTRYPOINT ["sh", "-c", "npx serve /app/dist"]