FROM amazonlinux:2

ENV LANG=en_US.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app/

RUN curl -sl https://rpm.nodesource.com/setup_8.x | bash -

RUN yum update -y && yum install -y wget nodejs npm python37 python37-pip

RUN ln -s /usr/bin/pip-3.7 /usr/bin/pip
RUN pip install pipenv

ENV PATH ./node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --dev --ignore-pipfile --system

COPY /src/ .
COPY . .
