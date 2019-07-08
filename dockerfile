FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache build-base # for uvloop
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone && date # default timezone
CMD ["python", "handlers.py"]