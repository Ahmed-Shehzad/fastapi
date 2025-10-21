-- Initialize database schema
-- This file is executed when the PostgreSQL container starts for the first time

-- Create additional schemas if needed
-- CREATE SCHEMA IF NOT EXISTS tasks;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;

-- Create extensions if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";