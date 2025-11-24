from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# my imports
from CozyWrites.config import settings
from CozyWrites.Models import Base

# this is the Alembic Config object
config = context.config

# Get DATABASE_URL from environment (for web deployments)
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Handle postgres:// vs postgresql:// prefix
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
else:
    # Fallback to settings
    database_url = (
        f"postgresql+psycopg://{settings.DATABASE_USERNAME}:"
        f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:"
        f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    )

# Set into alembic config
config.set_main_option("sqlalchemy.url", str(database_url))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
