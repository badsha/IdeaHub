-- This script is executed when the PostgreSQL container is first initialized.

-- Create the 'reporting' schema for analytics and reporting tables.
-- This is necessary before Alembic migrations can create tables within it.
CREATE SCHEMA IF NOT EXISTS reporting;