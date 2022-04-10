FROM python:3.8

ADD requirements.txt /app/requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r /app/requirements.txt

ADD . /app

WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV PYTHONPATH /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "pdlonline.wsgi"]