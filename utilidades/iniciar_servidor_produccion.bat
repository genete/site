@echo off
REM ============================================
REM Servidor HSQLDB - BASE DE DATOS PRODUCCIÓN
REM ============================================

set HSQL_PATH=W:\BDDATLIBRE\hslqdb
set DB_PRODUCCION=W:\BDDATLIBRE\bdat

echo ========================================
echo Iniciando Servidor HSQLDB PRODUCCION
echo Base de datos: %DB_PRODUCCION%\bdat
echo Puerto: 9001
echo Nombre BD: bdat
echo ========================================
echo.

java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server ^
  --database.0 file:%DB_PRODUCCION%\bdat ^
  --dbname.0 bdat ^
  --port 9001 ^
  --silent false ^
  --trace false

echo.
echo Servidor de produccion detenido.
pause