CREATE USER IF NOT EXISTS tdlog IDENTIFIED BY 'tdlog';
CREATE DATABASE IF NOT EXISTS autocomplete;
GRANT ALL PRIVILEGES ON autocomplete.* TO tdlog;