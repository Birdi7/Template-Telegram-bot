FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache build-base openssl-dev libffi-dev
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone # default timezone
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "-m", "core"]