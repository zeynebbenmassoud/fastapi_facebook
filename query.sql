CREATE DATABASE IF NOT EXISTS scrap_fdata
	CHARACTER SET = 'utf8'
	COLLATE = 'utf8_general_ci';
	
CREATE USER IF NOT EXISTS 'app'@'app' IDENTIFIED BY 'app';
		
GRANT ALL PRIVILEGES ON scrap_fdata.* To 'app'@'app';

FLUSH PRIVILEGES;

	
