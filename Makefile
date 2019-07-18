# The original file is here https://github.com/aiogram/EventsTrackerBot/blob/master/Makefile

gettext:
	pybabel extract core/ -o locales/bot.pot

createtexts:
	echo {en,ru} | xargs -n1 pybabel init -i locales/bot.pot -d locales -D bot -l

updatetext:
	pybabel update -d locales -D bot -i locales/bot.pot

compiletext:
	pybabel compile -d locales -D bot

migrate:
	alembic upgrade head

update:
	make gettext
	make updatetext

build:
	make compiletext
	make migrate
