@echo off
REM ================================================
REM Servidor HSQLDB - BASE DE DATOS PREPRODUCCIÓN
REM ================================================
set HSQL_PATH=W:\BDDATLIBRE\hslqdb
set DB_PREPRODUCCION=W:\BDDATLIBRE\preproduccion\bdat
echo ========================================
echo Iniciando Servidor HSQLDB PREPRODUCCION
echo Base de datos: %DB_PREPRODUCCION%\bdat
echo Puerto: 9003
echo Nombre BD: bdat_preproduccion
echo ========================================
echo.
java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server ^
  --database.0 file:%DB_PREPRODUCCION%\bdat ^
  --dbname.0 bdat_preproduccion ^
  --port 9003 ^
  --silent false ^
  --trace false
echo.
echo Servidor de preproduccion detenido.
pause