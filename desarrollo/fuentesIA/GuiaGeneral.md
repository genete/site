# PROYECTO BDDATLIBRE

## Propósito

El propósito de este proyecto es desarrollar una base de datos y un interfaz para gestionar tramitaciones de expedientes de solicitudes de instalaciones de alta tensión.

El proyecto tiene dos retos principales. Uno el desarrollo técnico de la base de datos y el interfaz y dos la definición de la lógica de negocio de la tramitación de expedientes.

## Desarrollo de la base de datos

En el desarrollo de la base de datos vamos a enfrentarnos a la organización de la información, así como la necesidad de concurrencia de los usuarios. Para la organización de la información se ha estudiado la lógica del proceso de tramitación de expedientes, y la relación entre la información que se maneja. De esta forma, la estructura de la base de datos está relacionada con la forma de tramitación de los expedientes. Primero analizaremos las claves desde el punto de vista técnico, de implementación, conociendo las necesidades del entorno en el que vamos a desarrollar.

### Claves técnicas

- **Entorno**: usuarios con Windows 11(máximo 15) en red, con servidor de archivos mantenido por el entorno empresarial.
- **Base de datos**: HSLQDB en servidor. EL servidor se ejecuta inicialmente en el PC de un usuario en red y los clientes son otros usuarios en red. La base de datos y otros archivos se alojan en el servidor de red. Se pretende que en el futuro el servidor de bases de datos se ejecute en el servidor central. Contiene las tablas y consultas necesarias.
- **Interfaz de cliente**: Documento LibreOffice Base conectado a la base de datos externa. Contiene los formularios y macros. Las macros son importadas de solo lectura desde un almacén en el servidor central. Eventualmente podría tener consultas creadas por el propio usuario pero alojadas en el propio documento, no en el servidor.
- **Estructura de ficheros**: cada usuario tiene una unidad W que apunta a un directorio del servidor. Se garantiza lectura y escritura completa a cada usuario. La unidad se monta automáticamente en cada PC.
- **Desarrollo**: se estructura la base de datos , se programan las macros y diseñan los formularios en el directorio /desarrollo y luego para poner en producción hay que dar una serie de pasos que tenemos que definir más adelante.
- **Soporte**: Para recibir soporte por parte de la IA para desarrollar la base de datos y su infraestructura, hay que proporcionarle una conjunto de ficheros a la misma. Se ubicarán en desarrollo/fuentesIA.

### Estructura de ficheros

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
| bdat | Aloja los ficheros .script y .properties de la base de datos |
| desarrollo | Dispone todos los directorios necesarios para desarrollar la base de datos |
| desarrollo/bdat | Base de datos en desarrollo |
| desarrollo/documentos | Contiene los documentos para el desarrollador |
| desarrollo/fuentesIA | Contiene los documentos necesarios para darle información a la IA, por ejemplo este documento en formato MarkDown. |
| desarrollo/interfaz | Documentos .odb de desarrollo |
| desarrollo/macros | Macros de desarrollo para formularios. |
| desarrollo/plantillas | Plantillas .ott de desarrollo |
| desarrollo/utilidades | Scripts utiles (bat, py, etc.). Sirven para ejecutar el servidor de la base de datos en desarrollo y otras utilidades para convertir documentos. |
| documentos | Documentos y guías para el usuario final |
| hsqldb | Ficheros Java (.jar) para ejecutar el servidor de bases de datos HSQLDB. |
| Interfaz | Copias en producción de los interfaces .odb de usuarios para conectarse a la base de datos. Hay dos tipos de usuarios (tramitador y supervisor) con privilegios diferenciados por tablas. |
| macros | Macros BASIC de LibreOffice para importar en solo lectura por los interfaces de los usuarios. |
| plantillas | Documentos .ott en producción. |
| utilidades | fichero bat para iniciar el servidor. |

### Documentos a proporcionar a la IA

A la IA le debemos proporcionar los siguientes documentos para que nos proporcione soporte y constituya una fuente de conocimiento. Los documentos los generamos en desarrollo/documentos y con la utilidad de conversión de .odt a .md los convertimos en el formato MarkDown entendible por la IA.

Los documentos, su tipo y su ubicación se listan a continuación:

|  |  |  |  |
|----|----|----|----|
| NOMBRE | TIPO | PROCEDENCIA | UTILIDAD |
| bdat.script | SQL | Directorio desarrollo/bdat | Conocer estructura base datos |
| content.xml | XML | desarrollo/interfaz/\*.odb/ | Conocer estructura \*.odb |
| content.xml | XML | desarrollo/interfaz/\*.odb/forms/Obj\*\*/ | Conocer formularios del odb |
| script-lc.xml | XML | desarrollo/interfaz/\*.odb/Basic/ | Conocer las librerías del odb |
| manifiest.xml | XML | desarrollo/interfaz/\*.odb/META-INF/ | Proporciona listado de todos los xml en el odb |
|  |  |  |  |

Los archivos se los proporcionamos en formato directo al subirlo a la IA. Debemos cambiar el nombre para que lo pueda interpretar en el caso de que mantenga el mismo, por ejemplo para el caso de content.xml. En este caso antepondremos el nombre del Objnn. Por ejemplo Obj11content.xml, corresponde con el content.xml del formulario Obj11 en el fichero odb.

## Lógica de la tramitación de expedientes

Los expedientes de solicitudes de instalaciones de alta tensión se tramitan conforme a una normativa específica y mediante las reglas establecidas en las leyes sectoriales y la ley de procedimiento administrativo. Tras analizar los distintos tipos de procedimientos se concluye que la tramitación tiene correlación con una serie de conceptos: expediente, solicitud, proyecto, fase, trámite y tarea.

### Relación expediente, solicitud, proyecto, fase, trámite y tarea

Se tramita un solo expediente cada vez, que dispone de un número único (por mantener el historial el número usado no será el ID del expediente en la base de datos, si no un número paralelo generado desde un valor base tomado de otra base de datos existente). Cada expediente tiene un proyecto asociado. Un proyecto puede tener modificaciones siempre que no desvirtúen su esencia (finalidad). Cada expediente puede tener diferentes solicitudes (autorización administrativa previa, autorización administrativa de construcción, etc.) sobre el mismo proyecto (o el proyecto con uno o más modificados). Cada solicitud pasa por diferentes fases (ANÁLISIS SOLICITUD, INFORMACIÓN PÚBLICA, CONSULTAS, etc.) aunque hay casos en que puede haber más de una fase activa al mismo tiempo. Cada fase puede tener uno o más trámites (por ejemplo la fase de información pública puede tener el trámite de publicación en BOE y el trámite de publicación en BOP) y cada trámite puede tener una o más tareas (redactar anuncio, poner en firma, notificar, esperar plazo, etc.)

### Estructura de negocio de la tramitación

En nuestro caso queremos que la lógica de negocio no sea rígida, restringiendo lo que se puede o no se puede hacer en cada solicitud, fase, trámite, etc. de forma que no exista margen de maniobra para el usuario en tomar decisiones dentro de lo posible. Deseamos que la lógica sea definida de la siguiente forma:

1.  En cualquier estado o situación del expediente, es posible hacer cualquier cosa que no esté expresamente prohibida. En lugar de listar lo únicamente permitido, listar lo expresamente prohibido y permitir que se pueda hacer cualquier operación mientras no esté expresamente prohibida. Por ejemplo, una prohibición genérica sería que no se puede finalizar una fase si quedan trámites sin finalizar. Otra prohibición sería que no se puede iniciar la fase resolver si no se ha finalizado la fase análisis solicitud)
2.  Las prohibiciones que definen la lógica de la tramitación ha de obtenerse de valores definidos en tablas, no internamente escrito en el código. De esta forma la modificación de un precepto legal (y por tanto la lógica del procedimiento) no requiere modificar macros si no que solo requiere modificar los datos de las prohibiciones del procedimiento. Esto hace que el sistema se adapte rápidamente a los cambios.
