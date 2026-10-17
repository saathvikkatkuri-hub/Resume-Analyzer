
from database import engine, Base
from database_models import ResumeAnalysis

# Create tables defined in our database models
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
print("Tables:", list(Base.metadata.tables.keys()))
