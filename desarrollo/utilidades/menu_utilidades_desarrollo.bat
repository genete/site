@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:MENU
cls
echo ═══════════════════════════════════════════════════════════════
echo    MENÚ DE UTILIDADES DE DESARROLLO - BDDATLIBRE
echo ═══════════════════════════════════════════════════════════════
echo.
echo  [1] Convertir ODT a Markdown
echo  [2] Genera bdat.script.txt (requiere SCRIPT 'W:/BDDATLIBRE/desarrollo/fuentesIA/bdat.script.temp';)
echo  [3] Extraer formularios a JSON
echo  [4] Consolidar módulos BASIC
echo  [5] Extraer datos maestros
echo  [6] Iniciar servidor de desarrollo
echo.
echo  ───────────────────────────────────────────────────────────────
echo  [7] Ejecutar TODAS las utilidades de extracción
echo  ───────────────────────────────────────────────────────────────
echo.
echo  [0] Salir
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
set /p opcion="Seleccione una opción: "

if "%opcion%"=="1" goto CONVERTIR_ODT
if "%opcion%"=="2" goto LIMPIAR_SCRIPT
if "%opcion%"=="3" goto EXTRAER_FORMULARIOS
if "%opcion%"=="4" goto CONSOLIDAR_BASIC
if "%opcion%"=="5" goto EXTRAER_MAESTROS
if "%opcion%"=="6" goto SERVIDOR
if "%opcion%"=="7" goto TODAS_EXTRACCIONES
if "%opcion%"=="0" goto FIN
goto MENU

:CONVERTIR_ODT
cls
echo ═══════════════════════════════════════════════════════════════
echo  CONVERTIR ODT A MARKDOWN
echo ═══════════════════════════════════════════════════════════════
echo.
call ConvertidorODT-MD.bat
echo.
pause
goto MENU

:LIMPIAR_SCRIPT
cls
echo ═══════════════════════════════════════════════════════════════
echo  LIMPIAR SCRIPT SQL
echo ═══════════════════════════════════════════════════════════════
echo.
python limpia_script.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Falló la limpieza del script
) else (
    echo.
    echo [OK] Script limpiado correctamente
)
echo.
pause
goto MENU

:EXTRAER_FORMULARIOS
cls
echo ═══════════════════════════════════════════════════════════════
echo  EXTRAER FORMULARIOS A JSON
echo ═══════════════════════════════════════════════════════════════
echo.
echo Se abrirá un cuadro de diálogo para seleccionar el archivo .odb
echo.
python extraer_formularios_v5.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Falló la extracción de formularios
) else (
    echo.
    echo [OK] Formularios extraídos correctamente
)
echo.
pause
goto MENU

:CONSOLIDAR_BASIC
cls
echo ═══════════════════════════════════════════════════════════════
echo  CONSOLIDAR MÓDULOS BASIC
echo ═══════════════════════════════════════════════════════════════
echo.
set /p archivo_odb="Ingrese la ruta del archivo ODB: "
if exist "%archivo_odb%" (
    python consolidar_modulos_basic.py "%archivo_odb%"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Falló la consolidación de módulos
    ) else (
        echo.
        echo [OK] Módulos consolidados correctamente
    )
) else (
    echo.
    echo [ERROR] No se encontró el archivo: %archivo_odb%
)
echo.
pause
goto MENU

:EXTRAER_MAESTROS
cls
echo ═══════════════════════════════════════════════════════════════
echo  EXTRAER DATOS MAESTROS
echo ═══════════════════════════════════════════════════════════════
echo.
python extraer_datos_maestros.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Falló la extracción de datos maestros
) else (
    echo.
    echo [OK] Datos maestros extraídos correctamente
)
echo.
pause
goto MENU

:SERVIDOR
cls
echo ═══════════════════════════════════════════════════════════════
echo  INICIAR SERVIDOR DE DESARROLLO
echo ═══════════════════════════════════════════════════════════════
echo.
echo Iniciando servidor HSQLDB...
echo.
call iniciar_servidor_desarrollo.bat
goto MENU

:TODAS_EXTRACCIONES
cls
echo ═══════════════════════════════════════════════════════════════
echo  EJECUTAR TODAS LAS UTILIDADES DE EXTRACCIÓN
echo ═══════════════════════════════════════════════════════════════
echo.
set /p archivo_odb="Ingrese la ruta del archivo ODB: "
if not exist "%archivo_odb%" (
    echo.
    echo [ERROR] No se encontró el archivo: %archivo_odb%
    echo.
    pause
    goto MENU
)

echo.
echo ───────────────────────────────────────────────────────────────
echo  Paso 1/4: Limpiando script SQL...
echo ───────────────────────────────────────────────────────────────
python limpia_script.py
if %errorlevel% neq 0 (
    echo [ERROR] Falló limpia_script.py
    goto ERROR_TOTAL
)
echo [OK] Script limpiado

echo.
echo ───────────────────────────────────────────────────────────────
echo  Paso 2/4: Extrayendo formularios a JSON...
echo ───────────────────────────────────────────────────────────────
echo Se usará el archivo: %archivo_odb%
python extraer_formularios_v5.py "%archivo_odb%"
if %errorlevel% neq 0 (
    echo [ERROR] Falló extraer_formularios_v5.py
    goto ERROR_TOTAL
)
echo [OK] Formularios extraídos

echo.
echo ───────────────────────────────────────────────────────────────
echo  Paso 3/4: Consolidando módulos BASIC...
echo ───────────────────────────────────────────────────────────────
python consolidar_modulos_basic.py "%archivo_odb%"
if %errorlevel% neq 0 (
    echo [ERROR] Falló consolidar_modulos_basic.py
    goto ERROR_TOTAL
)
echo [OK] Módulos consolidados

echo.
echo ───────────────────────────────────────────────────────────────
echo  Paso 4/4: Extrayendo datos maestros...
echo ───────────────────────────────────────────────────────────────
python extraer_datos_maestros.py
if %errorlevel% neq 0 (
    echo [ERROR] Falló extraer_datos_maestros.py
    goto ERROR_TOTAL
)
echo [OK] Datos maestros extraídos

echo.
echo ───────────────────────────────────────────────────────────────
echo  Paso 5/5: Convirtiendo documentos ODT a Markdown...
echo ───────────────────────────────────────────────────────────────
call ConvertidorODT-MD.bat
echo [OK] Conversión completada

echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✓ TODAS LAS EXTRACCIONES COMPLETADAS EXITOSAMENTE
echo ═══════════════════════════════════════════════════════════════
echo.
echo Archivos generados en desarrollo/fuentesIA/
echo.
pause
goto MENU

:ERROR_TOTAL
echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✗ PROCESO INTERRUMPIDO POR ERRORES
echo ═══════════════════════════════════════════════════════════════
echo.
pause
goto MENU

:FIN
cls
echo.
echo Saliendo del menú de utilidades...
echo.
timeout /t 1 >nul
exit /b 0