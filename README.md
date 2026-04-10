# 🚀 Data Listing API

A production-ready REST API built with FastAPI for managing items (products, posts, etc.). Ready to connect with Flutter, React, or any frontend framework.

## ✨ Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete items
- ✅ **Pagination** - Limit and offset support
- ✅ **Search** - Filter items by title
- ✅ **Sorting** - Sort by price, creation date, or title
- ✅ **Input Validation** - Pydantic schemas with proper error messages
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **Auto Documentation** - Swagger UI & ReDoc
- ✅ **Error Handling** - Proper HTTP status codes
- ✅ **Logging** - Built-in application logging

## 📋 Requirements

- Python 3.10+
- pip (Python package manager)

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration (Optional)

Create a `.env` file in the project root:

```env
# Application Settings
APP_NAME=Data Listing API
APP_VERSION=1.0.0
DEBUG=False

# Database (SQLite by default)
DATABASE_URL=sqlite:///./app.db

# For PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS Origins (comma-separated)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# API Prefix
API_V1_PREFIX=/api/v1
```

## 🚀 Running the Application

### Development Mode (with auto-reload)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Alternative (using Python)

```bash
python -m app.main
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Check

```
GET /
GET /health
```

### Items CRUD (Base: `/api/v1`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/v1/items` | Create a new item | 201 Created |
| `GET` | `/api/v1/items` | Get all items (paginated) | 200 OK |
| `GET` | `/api/v1/items/{id}` | Get single item | 200 OK, 404 Not Found |
| `PUT` | `/api/v1/items/{id}` | Update item | 200 OK, 404 Not Found |
| `DELETE` | `/api/v1/items/{id}` | Delete item | 200 OK, 404 Not Found |

## 📝 Usage Examples

### Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Laptop Pro 15",
    "description": "High-performance laptop with 15-inch display",
    "price": 999.99
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Laptop Pro 15",
  "description": "High-performance laptop with 15-inch display",
  "price": 999.99,
  "created_at": "2026-04-10T12:00:00",
  "updated_at": "2026-04-10T12:00:00"
}
```

### Get All Items (with pagination)

```bash
# Basic list
curl "http://localhost:8000/api/v1/items"

# With pagination
curl "http://localhost:8000/api/v1/items?skip=0&limit=20"

# Search by title
curl "http://localhost:8000/api/v1/items?search=laptop"

# Sort by price (descending)
curl "http://localhost:8000/api/v1/items?sort_by=price&sort_order=desc"
```

**Response:**
```json
{
  "items": [...],
  "total": 50,
  "limit": 10,
  "offset": 0
}
```

### Get Single Item

```bash
curl "http://localhost:8000/api/v1/items/1"
```

### Update an Item

```bash
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Laptop Pro 15",
    "price": 1099.99
  }'
```

### Delete an Item

```bash
curl -X DELETE "http://localhost:8000/api/v1/items/1"
```

**Response:**
```json
{
  "message": "Item with ID 1 deleted successfully",
  "status_code": 200
}
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup & session management
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database CRUD operations
│   └── routes/
│       ├── __init__.py
│       └── item_routes.py   # Item API endpoints
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (create this)
├── app.db                  # SQLite database (auto-created)
└── README.md               # This file
```

## 🗄️ Database

### Development (SQLite)

By default, the app uses SQLite for easy development. The database file (`app.db`) is created automatically.

### Production (PostgreSQL)

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/your_database
   ```

## 🔧 Configuration

All settings are managed in `app/config.py` and can be overridden via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Data Listing API |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Enable debug mode | False |
| `DATABASE_URL` | Database connection string | sqlite:///./app.db |
| `CORS_ORIGINS` | Allowed frontend origins | ["http://localhost:3000"] |
| `API_V1_PREFIX` | API base path | /api/v1 |

## 🧪 Testing with Flutter

This API is ready for Flutter integration:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

const String baseUrl = 'http://localhost:8000/api/v1';

// Fetch items
Future<List<dynamic>> getItems() async {
  final response = await http.get(Uri.parse('$baseUrl/items'));
  final data = json.decode(response.body);
  return data['items'];
}

// Create item
Future<Map<String, dynamic>> createItem(Map<String, dynamic> item) async {
  final response = await http.post(
    Uri.parse('$baseUrl/items'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode(item),
  );
  return json.decode(response.body);
}
```

## 📊 Query Parameters

### GET /api/v1/items

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Number of items to skip |
| `limit` | int | 10 | Items per page (1-100) |
| `search` | string | null | Search by title |
| `sort_by` | string | null | Sort field (price, created_at, title) |
| `sort_order` | string | asc | Sort direction (asc, desc) |

## 🔒 Error Handling

The API returns proper error responses:

```json
{
  "detail": "Item with ID 999 not found"
}
```

Validation errors include field-specific messages:

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

## 🚢 Deployment

### Using Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t data-api .
docker run -p 8000:8000 data-api
```

## 📝 Notes

- Database tables are created automatically on startup
- All timestamps are in UTC
- Items support partial updates (only send fields you want to change)
- Price must be greater than 0
- Title is required and limited to 255 characters

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - Feel free to use this project for your own purposes.

---

**Built with ❤️ using FastAPI**
