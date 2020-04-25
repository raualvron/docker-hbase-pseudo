FROM ubuntu:18.04
MAINTAINER Raul Alvarez Roncel <ralvron@upo.es>
LABEL version="0.1"
LABEL description="Hbase pseudo-distributed mode"

#System
ENV HBASE_VERSION=2.1.2
ENV HBASE_HOME=/hbase-${HBASE_VERSION}


RUN apt update \
    && apt -y install software-properties-common ssh openssh-server vim

# Install Java
RUN apt -y install openjdk-8-jdk  \
    && update-java-alternatives -s java-1.8.0-openjdk-amd64

# Install Python, Pip and HappyBase
RUN apt-get update && apt-get install -y python python3.5 python-pip
RUN pip install happybase pip --upgrade --force-reinstall

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/

#Download hbase
RUN wget https://archive.apache.org/dist/hbase/${HBASE_VERSION}/hbase-${HBASE_VERSION}-bin.tar.gz
RUN tar -zxvf hbase-${HBASE_VERSION}-bin.tar.gz
RUN rm hbase-${HBASE_VERSION}-bin.tar.gz

#Hbase configuration
COPY config/* /config/
COPY config/hbase-site.xml ${HBASE_HOME}/conf
COPY config/hbase-env.sh ${HBASE_HOME}/conf

#Start hbase pseudo distributed mode
COPY script/ /script/
CMD /bin/bash /script/start-pseudo.sh && /bin/bash

# Hbase ports 
# Zookeeper Client Port
EXPOSE 2181
# HMaster Ports:
EXPOSE 16000 16001 
# WebUI Port
EXPOSE 16010 16012 16013
# Region servers Ports
EXPOSE 16030 16032 16033 16034 16035

RUN echo 'alias shellhb="$HBASE_HOME/bin/hbase shell"' >> ~/.bashrc
RUN echo 'alias createdb="python /script/python/createTable.py /script/csv/SET-dec-2013.csv"' >> ~/.bashrc
RUN echo 'alias exportdb="python /script/python/exportTable.py"' >> ~/.bashrc
RUN echo 'alias deletedb="python /script/python/deleteTables.py"' >> ~/.bashrc
RUN echo 'alias catoutput="cat /script/csv/output.csv"' >> ~/.bashrc

# Commands:
# docker build -t ralvron/hbase_pseudo .
# docker run -it --name hbasepseudo -P ralvron/hbase_pseudo   
# docker run -it --name hbasepseudo --hostname=hbasepseudo -P ralvron/hbase_pseudo 
# docker run -it --name hbasepseudo -p 2181:2181 -p 16000:16000 -p 16010:16010 -p 16020:16020 -p 16030:16030 ralvron/hbase_pseudo
