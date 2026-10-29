# Django REST Framework Pagination

This project implements and tests Page Number Pagination, Global Pagination settings, and Custom Pagination in Django REST Framework.

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Populate test articles (creates 60 articles: 52 published, 8 drafts):
```bash
python manage.py populate_articles
```

5. Run development server:
```bash
python manage.py runserver
```

## Running Tests

Execute the automated test suite:
```bash
python manage.py test
```

## Endpoints

- `GET /api/articles/` - Task 1 & Task 2: Standard global pagination (15 items default, dynamic `page_size`, max 50).
- `GET /api/articles/custom/` - Task 3: Custom pagination (8 items default, `page_info` and `items_info`, input validation).

