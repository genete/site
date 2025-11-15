@echo off
REM ============================================
REM Servidor HSQLDB - BASE DE DATOS DESARROLLO
REM ============================================

set HSQL_PATH=W:\BDDATLIBRE\hsqldb
set DB_DESARROLLO=W:\BDDATLIBRE\desarrollo\bdat

echo ========================================
echo Iniciando Servidor HSQLDB DESARROLLO
echo Base de datos: %DB_DESARROLLO%\bdat
echo Puerto: 9002
echo Nombre BD: bdat_desarrollo
echo ========================================
echo.

java -cp "%HSQL_PATH%\hsqldb-jdk8.jar" org.hsqldb.server.Server ^
  --database.0 file:%DB_DESARROLLO%\bdat ^
  --dbname.0 bdat_desarrollo ^
  --port 9002 ^
  --silent true ^
  --trace false

echo.
echo Servidor de desarrollo detenido.
pause