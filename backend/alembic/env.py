from database import Base  # now resolves correctly via sys.path hack
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
import os
import sys
from logging.config import fileConfig

# Ensure project root is on sys.path so we can import database and models
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Load environment variables from .env in project_root
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the SQLAlchemy URL with our DATABASE_URL env var
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# Add your model's MetaData object here for 'autogenerate' support

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
