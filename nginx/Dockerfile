FROM nginx:1.17

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d

RUN apt-get update
RUN apt-get install -y openssl