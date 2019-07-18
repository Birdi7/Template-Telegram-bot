### Template for a telegram bot using [aiogram](https://github.com/aiogram/aiogram) and [umongo](https://github.com/Scille/umongo)

#### Running

This project can be run purely with python,
but also supports the deployment using [docker-compose](docker_compose)
 
Purely python running:

0.1. Check if you have the right version of python. Python3 -V should output 3.7+.

   If you are on Windows, remove uvloop from [requirements.txt](requirements.txt)
   as this lib doesn't work on this OS.

1. Copy an example environment file with `cp example.env local.env`
2. Add environment variables from `local.env` to your local os. 
   If you're on UNIX, you can add them only for the python running.
   Read [here](https://opensourcehacker.com/2012/12/13/configuring-your-python-application-using-environment-variables/)
   about it
3. Create a virtual environment with `python3 -m virtualenv venv`. 
4. Run `source venv/bin/activate` to activate the venv
5. Install modules with `pip install -r requirements.txt`
6. Run bot with `python handlers.py` 

With docker-compose:
1. Copy an example environment file with `cp example.env local.env`
2. Modify the local environment file named `.env`   
1. Run `docker-compose up -d --build`


[docker_compose]: <https://docs.docker.com/compose/>
