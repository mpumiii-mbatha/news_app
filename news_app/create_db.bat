@echo off
echo Creating database newsapp_db...

mysql -u root -p < create_database.sql

echo Done!
pause