## Run project using docker


0. setup docker-compose
0. bash: `make up`
0. bash: `make generate_data`


## Run project locally

0. create virtualenv: `virtualenv -p python3.8 venv`
0. install python packages: `pip install -r requirements/local.txt`
0. create PostgreSQL database
0. copy `env_example` into `.env` and replace variables
0. apply migrations: `python src/manage.py migrate`
0. generate random data: `python src/manage.py generate_random_data`
0. start dev server: `python src/manage.py runserver`
