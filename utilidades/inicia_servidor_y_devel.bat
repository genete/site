@echo off
set HSQL_PATH=W:\BDDATLIBRE\hslqdb
set DB_PRODUCCION=W:\BDDATLIBRE\bdat
set DB_DESARROLLO=W:\BDDATLIBRE\desarrollo\bdat

java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server ^
  --database.0 file:%DB_PRODUCCION%\bdat ^
  --dbname.0 bdat ^
  --database.1 file:%DB_DESARROLLO%\bdat ^
  --dbname.1 bdat_desarrollo ^
  --port 9001

pause