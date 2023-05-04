# Getting Started

## Usage

## Development

### Project Strucuture

```bash
.
├── README.md
├── docs
│   ├── index.md
├── mkdocs.yml
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── repository
│   │   ├── __init__.py
│   │   ├── celery_repository.py
│   │   ├── models.py
│   │   ├── redis_repository.py
│   │   └── spider.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   ├── tvtime.py
│   │   └── user.py
│   └── service
│       ├── __init__.py
│       ├── tvtime_data.py
│       └── tvtime_scraper.py
│  
└── tests
    ├── assets
    │   └── data.json
    ├── test_app.py
    └── test_spider.py
```

## Architecture & API

![Architecture](https://drive.google.com/uc?export=view&id=1EOAMykKKfjmsLSeXlrIw4QOsD3BSgAZU)

![API](https://drive.google.com/uc?export=view&id=1AhywkAhRfkQv_xdmGha4vFxjuqfKLAkk)

---
