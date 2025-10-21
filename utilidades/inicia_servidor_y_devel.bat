@echo off
set HSQL_PATH=W:\BDDATLIBRE\hslqdb
set DB_PATH=W:\BDDATLIBRE\BD
java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server --database.0 file:%DB_PATH%\bdat --dbname.0 bdat --database.1 file:%DB_PATH%\bdatdevel --dbname.1 bdatdevel --port 9001
pause
