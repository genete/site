@echo off
set HSQL_PATH=W:\BDDATLIBRE\hslqdb
set DB_PATH=W:\BDDATLIBRE\BD\bdat
java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server --database.0 file:%DB_PATH%\bdat --dbname.0 bdat --port 9001
pause