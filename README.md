# MM Order API

A FastAPI-based order management system with PostgreSQL database, built with modern Python tooling using `uv` package manager and containerized with Docker.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **UV Package Manager** - Ultra-fast Python package installer and resolver
- **Docker & Docker Compose** - Containerization support
- **Multi-stage Docker builds** - Optimized container images

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- UV package manager

## 🛠️ Installation

### 1. Install UV Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Add UV to your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify installation:
```bash
uv --version
```

### 2. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt install postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. Database Setup

```bash
# Switch to postgres user
sudo -i -u postgres

# Access PostgreSQL
psql

# Create database and user
CREATE DATABASE shop_order_api;
CREATE USER shopuser WITH ENCRYPTED PASSWORD 'secret123';
GRANT ALL PRIVILEGES ON DATABASE shop_order_api TO shopuser;

# Set password for postgres superuser (optional)
ALTER USER postgres PASSWORD 'postgres123';
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd mm-order-api
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Environment Configuration
Create a `.env` file:
```bash
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/shop_order_api
```

### 4. Run the application
```bash
uv run --env-file .env python app/main.py
```

The API will be available at: `http://localhost:8000`

## 📖 API Documentation

Once the application is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## 🐳 Docker Usage

### Build the Docker image
```bash
docker build -t mm-shop-api:latest .
```

### Run with Docker

**Linux (with host networking):**
```bash
docker run --network host \
  -e DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/shop_order_api \
  mm-shop-api:latest
```

**macOS/Windows:**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres123@host.docker.internal:5432/shop_order_api \
  mm-shop-api:latest
```

### Docker Compose

Run the entire stack with Docker Compose:
```bash
docker compose up -d
```

This will start both the application and PostgreSQL database.

## 📊 Docker Image Optimization

Our multi-stage Docker build significantly reduces image size:

| Version | Build Type | Size |
|---------|------------|------|
| v0.0.1  | Single-stage | 290MB |
| v0.0.2  | Single-stage | 290MB |
| v0.0.3  | Multi-stage | 149MB |

**48% size reduction** achieved through multi-stage builds!

## 🔌 API Endpoints

### General
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Orders
- `GET /orders` - List all orders (with optional status filter)
- `GET /orders/{order_id}` - Get a specific order by ID
- `POST /orders` - Create a new order

### Example: Create Order

```bash
curl -X POST "http://localhost:8000/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_name": "Alice Smith",
       "product_name": "MacBook Pro",
       "quantity": 1,
       "price": 2499.00,
       "status": "pending"
     }'
```

### Example: Get Order by ID

```bash
curl http://localhost:8000/orders/1
```

### Example: List Orders with Status Filter

```bash
# Get all orders
curl http://localhost:8000/orders

# Get orders with specific status
curl "http://localhost:8000/orders?status=pending"
```

### Example: Health Check

```bash
curl http://localhost:8000/health
```

**Health Check Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-24T00:03:44.004584",
  "database": "connected"
}
```

**Response:**
```json
[
  {
    "id": 1,
    "customer_name": "Alice Smith",
    "product_name": "MacBook Pro",
    "quantity": 1,
    "price": 2499,
    "status": "pending",
    "created_at": "2025-08-24T00:03:44.004584",
    "total_amount": 2499
  }
]
```

## 🏗️ Project Structure

```
mm-order-api/
├── app/
│   ├── __init__.py
│   └── main.py          # Main FastAPI application
├── .env                 # Environment variables
├── .dockerignore       # Docker ignore rules
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Multi-stage Docker build
├── pyproject.toml      # Project dependencies and metadata
├── README.md           # This file
└── uv.lock            # Dependency lock file
```

## 🔧 Development

### Install development dependencies
```bash
uv sync --dev
```

### Run tests
```bash
uv run pytest
```

### Code formatting
```bash
uv run black .
uv run isort .
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `DEBUG` | Enable debug mode | `False` |
| `LOG_LEVEL` | Logging level | `info` |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [UV](https://github.com/astral-sh/uv) for ultra-fast Python package management
- [PostgreSQL](https://www.postgresql.org/) for the robust database system