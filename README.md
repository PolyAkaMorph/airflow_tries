# airflow_tries
Airflow tries and attempts

links 
habr.com/ru/company/ivi/blog/456630/ - detailed install
github.com/puckel/docker-airflow - alternative image
habr.com/ru/company/mailru/blog/344398/ - jinja, hql-sql
docs.microsoft.com/ru-ru/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v - enable hyper-v
docs.docker.com/docker-for-windows/install/ - docker install

_requirements: win 10, at least 4 gb ram, 64 bit cpu and internet required
enable hyper-v (link above)
virtualization must be enabled - check it in task manager\performance\cpu (if not -  activate it in bios)
install docker (link above)
use linux containers_

_start win power shell (it was not working from first time, probably some internet lag) - this uploads ubuntu image_
docker pull ubuntu

_create and run docker, open bash, open and map port 8080 to it_
docker run -it -p 8080:8080 --name test ubuntu:latest bash
_or check existing ones with_
docker ps -a
_and run it_
docker start %CONTAINER_NAME% -i
_or check only running ones with_
docker ps
_and open shell to it using_
docker container exec -it %CONTAINER_NAME% /bin/bash/
_now we have shell to ubuntu opened. you have root privilegies, so care_
_update info about packages, install python and pip_
apt-get update && apt-get install -y python3.6 python3.6-dev && update-alternatives --install /usr/bin/python3 python3.6 /usr/bin/python3.6 0 && apt-get -y install python3-pip
_now get airflow and dependencies_
pip3 install pandas==0.20.3 apache-airflow==1.10.8 werkzeug==0.16.0
_run airflow db_
airflow initdb
_run scheduler_
airflow scheduler
_and web server with port that we mapped before_
airflow webserver --port 8080

_Alternative way with prepared Debian image from github.com/puckel/docker-airflow _
_get image from dockerhub_
docker pull puckel/docker-airflow 
_run it with UI and DAG examples_
docker run -d -p 8080:8080 -e LOAD_EX=y puckel/docker-airflow
_take a look on UI using browser on host, visit localhost:8080 - if it not working, something was wrong_
_make dir for DAGs in container's shell_
mkdir /root/airflow/dags
_set env var airflow_home_
export AIRFLOW_HOME=~/airflow
_set airflow var json_home_
airflow variables -s json_home $AIRFLOW_HOME/dags/task.json
_check name of your container with (run from host shell)_
docker ps
_copy json with tasks from host machine to running container (run from host shell)_
docker cp %HERE_MUST_BE_PATH_ON_HOST%\task.json %HERE_MUST_BE_NAME_OF_CONTAINER%:/root/airflow/dags/task.json
_copy python script from host machine to running container (run from host shell)_
docker cp %HERE_MUST_BE_PATH_ON_HOST%\run.py %HERE_MUST_BE_NAME_OF_CONTAINER%:/root/airflow/dags/run.py

#now in UI you can see new DAG.

ToDo:
airflow.cfg && airflow_home after start
xCom 
jinja

