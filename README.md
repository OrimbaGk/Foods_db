# Foods_db API

A practical python-based API application that establishes a working connection between a FastAPI/Uvicorn server and a local relational database. 

## Features
- **FastAPI Framework**: High-performance, clean asynchronous routing.
- **SQLAlchemy ORM**: Seamless translation between Python objects and database rows.
- **SQLite/PostgreSQL Integration**: Scalable backend data architecture.
- **Auto-generated Documentation**: Interactive API testing suite.

---

## Getting Started

Follow these instructions to set up and run the project locally on your machine.

### Prerequisites
Make sure you have Python 3.10+ installed on your system.

### Installation & Setup

1. **Clone the repository** (or navigate to your project directory):
   ```bash
   git clone https://github.com
   cd Foods_db
   ```

2. **Create and activate a virtual environment**:
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages**:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg
   ```

---

## Running the Application

Start the local development server using Uvicorn:

```bash
uvicorn main:app --reload
```

Once running, you can access the application at:
- **API Endpoint**: `http://127.0.0.1:8000`
- **Interactive API Documentation (Swagger UI)**: `http://127.0.0`

---

## File Structure

```text
Foods_db/
│
├── __pycache__/        # Compiled Python cache files
├── api.py             # Route handlers and API endpoint logic
├── main.py            # Application entry point and server startup
└── README.md          # Project documentation
```

---