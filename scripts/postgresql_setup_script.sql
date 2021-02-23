CREATE DATABASE opal_dev;
CREATE USER opal WITH PASSWORD 'use_a_strong_password';
ALTER ROLE opal SET client_encoding TO 'utf8';
ALTER ROLE opal SET default_transaction_isolation TO 'read committed';
ALTER ROLE opal SET timezone TO 'EST';
GRANT ALL PRIVILEGES ON DATABASE opal_dev TO opal;