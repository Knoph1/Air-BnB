-- creates MySQL database btcpbnb_test_db only if not existing
-- and gives privileges to user btcpbnb_test on 2 DB's
DROP DATABASE IF EXISTS btcpbnb_test_db;
DROP DATABASE IF EXISTS btcpbnb_dev_db;
CREATE DATABASE IF NOT EXISTS btcpbnb_dev_db;
GRANT ALL PRIVILEGES ON btcpbnb_dev_db.*
      TO btcpbnb_dev@localhost
      IDENTIFIED BY 'btcpbnb_dev_pwd';
GRANT SELECT ON performance_schema.*
      TO btcpbnb_dev@localhost
      IDENTIFIED BY 'btcpbnb_dev_pwd';
CREATE DATABASE IF NOT EXISTS btcpbnb_test_db;
GRANT ALL PRIVILEGES ON btcpbnb_test_db.*
      TO btcpbnb_test@localhost
      IDENTIFIED BY 'btcpbnb_test_pwd';
GRANT SELECT ON performance_schema.*
      TO btcpbnb_test@localhost
      IDENTIFIED BY 'btcpbnb_test_pwd';
