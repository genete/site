# PROYECTO BDDATLIBRE

## Propósito

El propósito de este proyecto es desarrollar una base de datos y un interfaz para gestionar tramitaciones de expedientes de solicitudes de instalaciones de alta tensión.

## Claves

- Entorno: usuarios con Windows 11(máximo 15) en red, con servidor de archivos mantenido por el entorno empresarial.
- Base de datos: HSLQDB en servidor. EL servidor se ejecuta inicialmente en el PC de un usuario en red y los clientes son otros usuarios en red. La base de datos y otros archivos se alojan en el servidor de red. Se pretende que en el futuro el servidor de bases de datos se ejecute en el servidor central. Contiene las tablas y consultas necesarias.
- Interfaz de cliente: Documento LibreOffice Base conectado a la base de datos externa. Contiene los formularios y macros. Las macros son importadas de solo lectura desde un almacén en el servidor central. Eventualmente podría tener consultas creadas por el propio usuario pero alojadas en el propio documento, no en el servidor.
- Estructura de ficheros: cada usuario tiene una unidad W que apunta a un directorio del servidor. Se garantiza lectura y escritura completa a cada usuario. La unidad se monta automáticamente.

## Estructura de ficheros

La estructura de ficheros parte de una ruta fija y tiene estos directorios:

W:\BDDATLIBRE

+---bdat

+---desarrollo

¦ +---bdat

¦ +---documentos

¦ +---fuentesIA

¦ +---interfaz

¦ +---macros

¦ +---plantillas

¦ +---utilidades

+---documentos

+---hslqdb

+---interfaz

¦ +---supervisor

¦ +---tramitador

+---macros

+---plantillas

+---utilidades

|  |  |
|----|----|
| DIRECTORIO | EXPLICACIÓN |
| bdat | aloja los ficheros .script y .properties de la base de datos |
| desarrollo | dispone todos los directorios necesarios para desarrollar la base de datos |
| desarrollo/bdat | base de datos en desarrollo |
| desarrollo/fuentesIA | contiene los documentos necesarios para darle información a la IA, por ejemplo este documento. |
| desarrollo/interfaz | documentos .odb de desarrollo |
| desarrollo/macros | macros de desarrollo |
| desarrollo/plantillas | plantillas .ott de desarrollo |
| desarrollo/utilidades | scripts utiles (bat, py, etc.). Sirven para ejecutar el servidor de la base de datos en desarrollo y otras utilidades para convertir documentos. |
| hsqldb |  ficheros .jar para ejecutar el servidor de bases de datos. |
| Interfaz | copias en producción de los interfaces .odb de usuarios para conectarse a la base de datos. Hay dos tipos de usuarios con privilegios diferenciados por tablas. |
| macros | macros BASIC de LibreOffice para importar en solo lectura por los interfaces de los usuarios. |
| plantillas | documentos .ott en producción. |
| utilidades | fichero bat para iniciar el servidor. |
