# TVTime Scrapy API

![Python Version](https://img.shields.io/badge/python-3.11.2-blue.svg)
![Work in Progress](https://img.shields.io/badge/Work-In%20Progress-red)
![Coverage Badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.badge&url=https%3A%2F%2Fgithub.com%2Fgiraycoskun%2Ftvtime-scrapy-api%2Factions%2Fruns%2F4801599532%2Flogs%2Fbadge%3Fevent%3Dcoverage)


It is a REST API that uses the Scrapy framework to work as unofficial TVTime API.

**Docs:** <https://giraycoskun.github.io/tvtime-scrapy-api/>

## Docker

## Local Development

```bash
poetry export -f requirements.txt --output requirements.txt --with docs,dev,test
```

```bash
uvicorn src.main:app --reload
```


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)