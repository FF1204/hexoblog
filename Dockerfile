FROM node:slim
# instal basic tool 
RUN apt-get update && apt-get install -y git ssh-client ca-certificates --no-install-recommends && rm -r /var/lib/apt/lists/*
# set time zone
RUN echo "Asia/Shanghai" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
RUN npm install
# install hexo
RUN npm install hexo-cli -g
# install hexo server
RUN npm install hexo-server
# set base dir
#RUN mkdir /hexo
# set home dir
#WORKDIR /hexo

EXPOSE 4000
#CMD ["/bin/bash"]
