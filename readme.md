## Template for a telegram bot

Dependencies:
 - [aiogram](https://github.com/aiogram/aiogram)
 - [umongo](https://github.com/Scille/umongo)
 
## Running

This project can be run purely with python,
but also supports the deployment using [docker](docker)
 
Purely python running:
1. Create a virtual environment with `python3 -m virtualenv venv`
2. Run `source venv/bin/activate` to activate the venv
3. Install modules with `pip install -r requirements.txt`
4. Run bot with `python handlers.py` 

With docker:
1. Build the image with `docker build -t=tg_bot .`
2. Run the image with `docker run -d tg_bot`


[docker]: <https://www.docker.com/>