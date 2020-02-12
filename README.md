# airflow_tries
Airflow tries and attempts
---------------------------------
links 
https:#habr.com/ru/company/ivi/blog/456630/ - detailed install
https:#github.com/puckel/docker-airflow - alternative image
https:#habr.com/ru/company/mailru/blog/344398/ - jinja, hql-sql
https:#docs.microsoft.com/ru-ru/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v - enable hyper-v
https:#docs.docker.com/docker-for-windows/install/ - docker install
---------------------------------
requirements: win 10, at least 4 gb ram, 64 bit cpu and internet required

enable hyper-v (link above)
virtualization must be enabled - check it in task manager\performance\cpu (if not -  activate it in bios)

install docker (link above)
use linux containers

start win power shell (it was not working from first time, probably some internet lag) - this uploads ubuntu image 

docker pull ubuntu
#create and run docker, open bash, open and map port 8080 to it
docker run -it -p 8080:8080 --name test ubuntu:latest bash
#or check existing ones with
docker ps -a
#and run it
docker start %CONTAINER_NAME% -i
#or check only running ones with
docker ps
#and open shell to it using
docker container exec -it %CONTAINER_NAME% /bin/bash/
#now we have shell to ubuntu opened. you have root privilegies, so care
#update info about packages, install python and pip
apt-get update && apt-get install -y python3.6 python3.6-dev && update-alternatives --install /usr/bin/python3 python3.6 /usr/bin/python3.6 0 && apt-get -y install python3-pip
#now get airflow and dependencies
pip3 install pandas==0.20.3 apache-airflow==1.10.8 werkzeug==0.16.0
#run airflow db
airflow initdb
#run scheduler
airflow scheduler
#and web server with port that we mapped before
airflow webserver --port 8080
-----------------------------------------------------------------
#Alternative way with prepared Debian image from https:#github.com/puckel/docker-airflow
#get image from dockerhub
docker pull puckel/docker-airflow 
#run it with UI and DAG examples
docker run -d -p 8080:8080 -e LOAD_EX=y puckel/docker-airflow
-----------------------------------------------------------------
#make dir for DAGs in container's shell
mkdir /root/airflow/dags
#set in ubuntu's shell variables:
#set env var airflow_home
export AIRFLOW_HOME=~/airflow
#set airflow var json_home
airflow variables -s json_home $AIRFLOW_HOME/dags/task.json

#take a look on UI using browser on host, visit localhost:8080 - if it not working, something was wrong

#check name of your container with (run from host shell)
docker ps
#copy json with tasks from host machine to running container (run from host shell)
docker cp %HERE_MUST_BE_PATH_ON_HOST%\task.json %HERE_MUST_BE_NAME_OF_CONTAINER%:/root/airflow/dags/task.json
#copy python script from host machine to running container (run from host shell)
docker cp %HERE_MUST_BE_PATH_ON_HOST%\run.py %HERE_MUST_BE_NAME_OF_CONTAINER%:/root/airflow/dags/run.py

#now in UI you can see new DAG.


ToDo:
airflow.cfg && airflow_home after start
xCom 
jinja

