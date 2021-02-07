## Introduction
The application flow happens as follows:
- User uploads a file.
- The application searches for all IPs contained in this file.
- A table is shown with all the information collected from the ips.
- If the ip is already inserted in the database, the results are retrieved from there. If it is not, it will insert into the database.
- If the ip is an exit node of the tor network, a tor icon will be shown just below the ip.

## Archtecture
Flask was chosen for its simplicity and agility of development.
The non-relational Redis database was chosen because it has the quickest and easiest way to cache values in a scalable way. The entered values are in a key/value format, fully compatible with a python dictionary

## Settings
The environment variables below will be consumed by settings.py, which will be inserted in all the respective containers responsible for execution.
There are default values for each of them, it is up to you whether you want to change it or not.
```
# WEB APPLICATION
export APP_PORT=8080

# THREADING
export THREAD_WORKERS=16

# REDIS
export REDIS_HOST=172.16.0.101
export REDIS_PORT=6379
export REDIS_PASSWORD=

# USE TOR NETWORK
export USE_TOR=False
export TOR_HASHED_PASSWORD=henrique

# RETRIES NUMBER BEFORE RETURN NONE
export HTTP_RETRIES=3
```

## How to run
```
docker-compose up --build
```

## Consideration
- Value filtering was not done using the back end, it is inserted in javascript using an input field above the table.
- Due to a limit of information capture with rdap, the tor network was used to circumvent requests coming from a new ip every time we are blocked.