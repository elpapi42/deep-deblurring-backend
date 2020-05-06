FROM python:3.6
LABEL maintainer="Bohorquez Whitman"

# Install app dependencies
COPY / /deep-deblurring-backend
WORKDIR /deep-deblurring-backend

RUN pip install -r requirements.txt

CMD ["gunicorn", "--config", "gunicorn.py", "deblurrer_api:create_app"]