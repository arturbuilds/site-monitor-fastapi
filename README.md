# Site Monitor API

A backend service for monitoring website availability and response status.

## Features

- Monitor website uptime
- Check HTTP status codes
- REST API built with FastAPI
- Asynchronous requests
- JSON responses

## Tech Stack

- Python
- FastAPI
- Uvicorn
- HTTPX
- Pydantic

## Installation

```bash
git clone https://github.com/arturbuilds/site-monitor-api.git
cd site-monitor-api

pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

or

```bash
python main.py
```

## API Example

```
GET /check?url=https://google.com
```

Example response

```json
{
    "status": "online",
    "status_code": 200,
    "response_time": 0.23
}
```

## Project Structure

```
site-monitor-api/
│
├── main.py
├── routers/
├── models/
├── schemas/
├── requirements.txt
└── README.md
```

## Future Improvements

- Database support
- Monitoring history
- Email notifications
- Dashboard
- Docker support
