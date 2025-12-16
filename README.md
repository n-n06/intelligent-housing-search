# Intelligent Housing Search <img src="/frontend/housing-app/public/app-logo.svg" width="20px">
> The **aim** of the project is to enable users to explore housing opportunities in particular regions and get insights about social, economical and ecological trends in these regions

![](|100)
<img src="/frontend/housing-app/public/app-logo.svg" width="100px">

## Objectives 🥅
📌 Gather reliable, up-to-date and true **data about different regions** of the city  
📌 Generate **metrics** to identify good places for rent/house purchase  
📌 Help users identify economical, social, ecological **trends on the housing market**  

## Backend 🧑‍💻
This is the backend service of the project, built with FastAPI, SQLAlchemy, and Alembic, using PostgreSQL + PostGIS as the database.
It is fully containerized with Docker Compose for easy setup and deployment.
### Structure
```bash
.
├── alembic                      # migrations
├── alembic.ini                  # migration configuration
├── auth.env                     # secret keys for hashing passwords
├── docker-compose.yml           # instructions to start the services
├── Dockerfile                   # build instructions for the app
├── entrypoint.sh                # Bash script to run migrations and start the app
├── pyproject.toml               # project description and dependencies
├── README.md                    # this file
├── src
│   ├── auth
│   │   ├── config.py            
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── models.py
│   │   ├── router.py            # authentication routes
│   │   ├── schemas.py
│   │   └── strategy.py
│   ├── config.py
│   ├── db.py
│   ├── __init__.py
│   ├── main.py                  # main script
│   ├── models.py
└── uv.lock

```

### Environment variables
#### `.env`
```
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=yourpassword
DB_NAME=app_db
```

#### `auth.env`
```
SECRET=your-secret-key
```

These are loaded automatically by Docker Compose — do not hardcode them in your `Dockerfile`.

### Running the Backend 🚀

1. Build and start the containers:
   ```
   docker compose up --build
   ```
2. Wait for migrations to complete(handled automatically in `entrypoint.sh`):

   ```
   Loading environment variables...
   Waiting for PostgreSQL to be ready at db:5432...
   Applying Alembic migrations...
   Starting FastAPI server on port 8000...
   ```

3. Access the API docs:
   ```
   http://localhost:8000/docs
   ```

### Useful Commands 💻

##### Rebuild everything (including migrations)
```bash
docker compose down -v
docker compose up --build
```

##### Run Alembic manually inside the container
```bash
docker compose exec app alembic upgrade head
```

##### Connect to PostgreSQL
```bash
docker compose db exec bash
psql -U $DB_USER -d $DB_NAME
```

##### View logs

```bash
docker compose logs -f app
docker compose logs -f db
```

### Development 🧰

##### Install dependencies locally (optional)
If you want to run outside Docker:
```
uv venv
source .venv/bin/activate
uv pip install -e .
```

##### Run Alembic locally
```
alembic upgrade head
```
##### Run FastAPI locally
```
uvicorn src.main:app --reload
```



## Frontend 👨‍🦲

### Running the Frontend 🚀

##### Install dependencies
```
npm install angular -g
npm install
```

##### Run the app
```
ng serve
```
##### View the frontend
Access the frontend by this address:
```
http://localhost:4200
```

## Contributors 🚴‍♂️
- Nursultan Zhantuar
- Alexander Tsoy
