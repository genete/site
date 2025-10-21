@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo  CONVERTIDOR ODT A MD PARA PERPLEXITY
echo ========================================
echo.

REM Verificar si se pasó un archivo como argumento (arrastrar y soltar)
if "%~1"=="" (
    REM No hay argumento, pedir archivo
    set /p "INPUT=Arrastra aqui el archivo ODT o escribe la ruta completa: "
    REM Quitar comillas si las hay
    set "INPUT=!INPUT:"=!"
) else (
    set "INPUT=%~1"
)

REM Verificar que el archivo existe
if not exist "!INPUT!" (
    echo.
    echo [ERROR] El archivo no existe: !INPUT!
    echo.
    pause
    exit /b 1
)

REM Verificar que pandoc está instalado
where pandoc >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Pandoc no esta instalado o no esta en el PATH
    echo Descarga Pandoc desde: https://pandoc.org/installing.html
    echo.
    pause
    exit /b 1
)

echo [OK] Pandoc detectado correctamente
echo.

REM Obtener información del archivo
for %%F in ("!INPUT!") do (
    set "INPUTDIR=%%~dpF"
    set "FILENAME=%%~nF"
)

REM Crear directorio de salida relativo
set "OUTPUTDIR=!INPUTDIR!..\fuentesIA"
set "OUTPUTFILE=!OUTPUTDIR!\!FILENAME!.md"

REM Crear directorio si no existe
if not exist "!OUTPUTDIR!" (
    echo Creando directorio: !OUTPUTDIR!
    mkdir "!OUTPUTDIR!"
)

echo Archivo de entrada:  !INPUT!
echo Archivo de salida:   !OUTPUTFILE!
echo.
echo Convirtiendo...
echo.

REM Ejecutar pandoc
pandoc "!INPUT!" -f odt -t gfm -o "!OUTPUTFILE!" --wrap=none --markdown-headings=atx --strip-comments --preserve-tabs

if errorlevel 1 (
    echo.
    echo [ERROR] La conversion fallo
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Conversion completada exitosamente
echo.

REM Preguntar si abrir el archivo
set /p "ABRIR=Deseas abrir el archivo markdown? (S/N): "
if /i "!ABRIR!"=="S" (
    start notepad.exe "!OUTPUTFILE!"
)

echo.
echo Presiona cualquier tecla para salir...
pausefuentes