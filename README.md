<img src="https://cdn-icons-png.flaticon.com/512/10194/10194172.png" width="10%">

# TVTime Scrapy API

![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![Work in Progress](https://img.shields.io/badge/Work-In%20Progress-red)
[![Coverage Status](https://coveralls.io/repos/github/giraycoskun/tvtime-scrapy-api/badge.svg?branch=main)](https://coveralls.io/github/giraycoskun/tvtime-scrapy-api?branch=main)

It is a REST API that uses the Scrapy framework to work as unofficial TVTime API.

**Docs:** <https://giraycoskun.github.io/tvtime-scrapy-api/>

**Reference:** <https://giraycoskun.github.io/tvtime-scrapy-api/reference/index/>

**Swagger UI:** <https://giraycoskun.github.io/tvtime-scrapy-api/openapi/>

## Docker

## Local Development

```bash
poetry export -f requirements.txt --output requirements.txt --with docs,dev,test
```

```bash
uvicorn src.main:app --reload
```

```bash
coverage run --source src -m pytest
```

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
