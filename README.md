# docker-hbase-pseudo

This repository contains DockerFile of HBase 2.1.2 in pseudo distributed

### Base Docker Image

Ubuntu

### HBase version supported

- [HBase 2.1.2](https://archive.apache.org/dist/hbase/2.1.2/)

### Build the required image

```
docker build -t ralvron/hbase_pseudo .
```

### Running container

```
docker run -it -P --name hbasepseudo ralvron/hbase_pseudo
```
```
docker run -it --hostname=hbasepseudo -p 2181:2181 -p 16010:16010 -p 16000:16000 -p 16001:16001 -p 16012:16012 -p 16013:16013 -p 16030:16030 -p 16032:16032 -p 16033:16033 -p 16034:16034 -p 16035:16035 ralvron/hbase_pseudo
```

### Hbase ports 
##### Zookeeper Client
Ports: 2181
##### HMaster
Ports: 16000 16001 
##### WebUI
Ports: 16010
##### Backup servers
Ports: 16012 16013
##### Region servers
Ports: 16030 16032 16033 16034 16035

### Alias on Docker Image
- Get access to the HBase shell
```
shellhb
```

- Import data into HBase by row and column using the CSV
```
createdb 2 2
```

- Delete HBase tables
```
deletedb
```

```
alias createdb="python /script/python/createTable.py /script/csv/SET-dec-2013.csv"
alias exportdb="python /script/python/exportTable.py"
alias deletedb="python /script/python/deleteTables.py"
alias catoutput="cat /script/csv/output"
```
