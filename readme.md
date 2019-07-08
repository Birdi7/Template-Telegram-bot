### Template for a telegram bot using [aiogram](https://github.com/aiogram/aiogram) and [umongo](https://github.com/Scille/umongo)

#### Running

This project can be run purely with python,
but also supports the deployment using [docker-compose](docker_compose)
 
Purely python running:
1. Create a virtual environment with `python3 -m virtualenv venv`
2. Run `source venv/bin/activate` to activate the venv
3. Install modules with `pip install -r requirements.txt`
4. Run bot with `python handlers.py` 

With docker-compose:
1. Run `docker-compose up -d --build`


[docker_compose]: <https://docs.docker.com/compose/>