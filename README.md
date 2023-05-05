<img src="https://cdn-icons-png.flaticon.com/512/10194/10194172.png" width="10%">

# TVTime Scrapy API

![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Work in Progress](https://img.shields.io/badge/Work-In%20Progress-red)
[![Coverage Status](https://coveralls.io/repos/github/giraycoskun/tvtime-scrapy-api/badge.svg)](https://coveralls.io/github/giraycoskun/tvtime-scrapy-api)

It is a REST API that uses the Scrapy framework to work as unofficial TVTime API.

**Docs:** <https://giraycoskun.github.io/tvtime-scrapy-api/>

**Reference:** <https://giraycoskun.github.io/tvtime-scrapy-api/reference/index/>

**Swagger UI:** <https://giraycoskun.github.io/tvtime-scrapy-api/openapi/>

## Security

As TvTime does not have an OAUTH Code Grant Flow, it is not possible to use the API with a token and thus it requires TVTime username and password. Therefore it is not up-to security standards and it cannot promise that without the oauth2.0 scheme.

However it only uses username and password to scrape data and does not store the password.

## Architecture

![Architecture](https://drive.google.com/uc?export=view&id=1EOAMykKKfjmsLSeXlrIw4QOsD3BSgAZU)

![API](https://drive.google.com/uc?export=view&id=1AhywkAhRfkQv_xdmGha4vFxjuqfKLAkk)

## Docker

```bash
docker pull redis/redis-stack
```

## Local Development

```bash
poetry export -f requirements.txt --output requirements.txt --with docs,dev,test
```

```bash
uvicorn src.main:app --reload
```

```bash
pytest -o log_cli=true -o log_cli_level=DEBUG 
```

```bash
coverage run --source src -m pytest
```

```bash
celery -A src.repository.celery_repository worker --concurrency 2 --loglevel=DEBUG
```

### TODO

- [ ] Add tests to cover data services & celery
- [ ] Add user authentication
- [ ] Add exception handling from scrapy
- [ ] Add exception handling from redis

## Reference

**FASTAPI**: <https://fastapi.tiangolo.com/>

**REDIS**: <https://redis.io/>

**CELERY**: <https://docs.celeryproject.org/en/stable/>

**SCRAPY**: <https://docs.scrapy.org/en/latest/>

---

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=fff&style=for-the-badge)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
