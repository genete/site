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

### Control de versiones 

El proyecto utiliza Git para control de versiones. Se hacen commits de los archivos principales cuando se consolidan cambios importantes. Esto permite:

- Volver a versiones anteriores si algo falla
- Tener historial de evolución del proyecto
- Trabajar de forma segura en desarrollo sin miedo a perder trabajo

Los archivos bajo control de versiones incluyen:

- Base de datos de desarrollo (bdat.script, bdat.properties)
- Interfaces .odb de desarrollo
- Macros (.xml)
- Scripts de utilidades (.py, .bat)
- Documentación (.md, .odt)
- Archivos fuente IA (JSON, XML, SQL, TXT)

### Estructura de ficheros

La estructura de ficheros parte de una ruta fija y tiene estos directorios:

W:\BDDATLIBRE

│

├───bdat

│

├───desarrollo

│ ├───bdat

│ ├───documentos

│ ├───fuentesIA

│ ├───interfaz

│ ├───macros

│ ├───plantillas

│ └───utilidades

│

├───preproduccion

│ ├───bdat

│ └───utilidades

│

├───documentos

│

├───hslqdb

│

├───interfaz

│ ├───supervisor

│ └───tramitador

│

├───macros

│

├───plantillas

│

└───utilidades

|  |  |
|----|----|
| DIRECTORIO | EXPLICACIÓN |
| bdat | Aloja los ficheros .script y .properties de la base de datos |
| desarrollo | Dispone todos los directorios necesarios para desarrollar la base de datos |
| desarrollo/bdat | Base de datos en desarrollo |
| desarrollo/documentos | Contiene los documentos para el desarrollador y para pasarlos a la IA |
| desarrollo/fuentesIA | Contiene los documentos necesarios para darle información a la IA, por ejemplo este documento en formato MarkDown. |
| desarrollo/interfaz | Documentos .odb de desarrollo |
| desarrollo/macros | Macros de desarrollo para formularios. |
| desarrollo/plantillas | Plantillas .ott de desarrollo |
| desarrollo/utilidades | Scripts utiles (bat, py, etc.). Sirven para ejecutar el servidor de la base de datos en desarrollo y otras utilidades para convertir documentos. |
| preproduccion | Dispone de los directorios necesarios para hacer las pruebas previas al despliegue en producción |
| preproduccion/bdat | Base de datos en preproducción |
| preproduccion/utilidades | Script para ejecutar el servidor de preproduccion |
| documentos | Documentos y guías para el usuario final |
| hsqldb | Ficheros Java (.jar) para ejecutar el servidor de bases de datos HSQLDB. |
| Interfaz | Copias en producción de los interfaces .odb de usuarios para conectarse a la base de datos. Hay dos tipos de usuarios (tramitador y supervisor) con privilegios diferenciados por tablas. |
| macros | Macros BASIC de LibreOffice para importar en solo lectura por los interfaces de los usuarios. |
| plantillas | Documentos .ott en producción. |
| utilidades | fichero bat para iniciar el servidor. |

### Documentos a proporcionar a la IA

A la IA le debemos proporcionar los siguientes documentos para que nos proporcione soporte y constituya una fuente de conocimiento. Los documentos los generamos en desarrollo/documentos y con la utilidad de conversión de .odt a .md los convertimos en el formato MarkDown entendible por la IA.

Los documentos, su tipo y su procedencia, coómo se obtiene y utilidad se listan a continuación:

| NOMBRE | TIPO | PROCEDENCIA | SCRIPT | QUÉ HACE | UTILIDAD |
|----|----|----|----|----|----|
| bdat.script.txt | SQL | bdat.script | *desarrollo/utilidades/limpia_script.py* | Se quitan las ordenes SQL tipo INSERT. Solicita con diálogo el .script a procesar y coloca el resultado donde elija el usuario*.* | Conocer estructura base datos |
| formularios_completo.json | JSON | \*.odb | *desarrollo/utilidades/extraer_formularios_v5.py* | Crea un json con los principales datos de formularios y controles. Solicita el fichero .odb y crea la salida en la misma ruta que el fichero odb. Este script además descomprime el fichero .odb en \_extract\_\*.odb en la misma ruta que el odb | Conocer estructura de formularios, controles, eventos y propiedades de los archivos .odb |
| NombreODB_modulos_consolidados.xml.txt | XML | desarrollo/interfaz/.odb | *desarrollo/utilidades/consolidar_modulos_basic.py* | Se obtiene con el script dándole el fichero .odb y la ruta de salida en la linea de comando. El prefijo varía según el ODB proporcionado. | Incluir el código fuente de las macros BASIC de LibreOffice en formato XML, legible por la IA |
| Documentos.md | MD | desarrollo/documentos/\*.odt | *desarrollo/utilidades/ConvertidorODT-MD.bat* | Conversión de .odt a .md con la macro. Pide la ruta al odb y lo coloca directamente en desarrollo/documentos. Usa pandoc internamente | Documentos de resumen de las directrices de desarrollo del proyecto así como explicaciones de la estructura de las bases de datos, la lógica de los procedimientos, etc. |
| datos_maestros.sql.txt | SQL | desarrolo/bdat/bdat.script | *desarrollo/utilidades/extraer_datos_maestros.py* | Extrae los datos INSERT de bdat.script de las tablas indicadas en fuentesIA/tablas_maestras.txt y lo coloca en fuentesIA/datos_maestros.sql.txt | Conocer los datos que definen la lógica de negocio: TIPOS_EXPEDIENTES, TIPOS_SOLICITUDES, etc |
| tablas_maestras.txt | TXT | Creada por el desarrollador | manual | Configuración del script extraer_datos_maestros.py | Contiene las tablas de datos maestros, que definen el negocio de la base de datos. |

El archivo JSON consolidado (formularios_completo.json) sustituye a los múltiples archivos XML de contenido (content.xml) y manifest.xml, proporcionando toda la información de formularios en un formato más estructurado y manejable.

Para mayor facilidad de uso se ha creado un script bat donde mediante menú se puede ejecutar cualquiera de los scripts anteriores: menu_utilidades_desarrollo.bat

### Proceso de iteración de desarrollo con la IA

Para la ayuda desde la IA en el proceso de desarrollo del proyecto, debo proporcionarle los archivos actualizados a medida que avanzo. El proceso sigue este flujo:

Ciclo de iteración:

Detecto necesidad → Le explico a la IA la necesidad y me ayuda a resolverla según el contexto actual de desarrollo → Realizo la implementación de la necesidad y la depuro de forma interactiva hasta que quedo satisfecho → Actualizo los ficheros pertinentes en las fuentes de la IA → Fin de iteración.

Control de versiones:

El proyecto está bajo control de versiones Git. Hago *commits* cuando hay cambios importantes consolidados. Esto garantiza que puedo volver atrás si algo no funciona.

Fases de desarrollo:

Esta forma de iterar con la IA para ir desarrollando todo el sistema tiene cuatro fases:

1.  Fase 1 – Estructura de datos

- - Definición de tablas maestras (tipos de datos estructurales)
  - Tablas de datos operacionales de expedientes
  - Sin lógica de negocio implementada (todo está permitido)
  - Enfoque: consolidar estructura de BD paso a paso

1.  Fase 2 – Interfaz de usuario

- - Formularios de introducción de datos
  - Macros de ayuda (navegación, filtrado, plantillas, apertura documentos)
  - Sin restricciones de lógica de negocio (el usuario controla qué hacer)
  - Enfoque: consolidar interfaz funcional paso a paso
  - Podría ponerse en producción al finalizar esta fase

1.  Fase 3 - Lógica de Negocio

- - Definición de tablas que configuran la lógica de negocio
  - Interfaz SUPERVISOR para gestionar esas tablas
  - Macros de validación basadas en consultas (no hardcoded)
  - *Despliegue progresivo* en producción de nuevas funcionalidades
  - *IMPORTANTE*: Aquí sí requiere mayor control porque ya hay usuarios y datos reales

1.  Fase 4 - Desarrollo continuo

- - Mejoras y nuevas funcionalidades
  - Base de datos en producción con usuarios activos
  - Proceso de actualización y despliegue definido

Dependencias entre archivos fuente IA:

Cuando modifico algo, debo actualizar los archivos correspondientes:

- Cambio en estructura BD → Regenerar: \`bdat.script.txt\`, \`formularios_completo.json\`
- Cambio en macros → Regenerar: \`NombreODB_modulos_consolidados.xml.txt\`
- Cambio en datos maestros → Actualizar (si procede) \`tablas_maestras.txt\`→ Regenerar: \`datos_maestros.sql.txt\`
- Cambio en formularios → Regenerar: \`formularios_completo.json\`

### Proceso de despliegue en producción

Para el despliegue en producción se necesitan tenemos los siguientes recursos:

Servidores de bases de datos de producción, preproducción y desarrollo. Los scripts se encuentran en sus carpetas correspondientes.

- Por definir

## Lógica de la tramitación de expedientes

Los expedientes de solicitudes de instalaciones de alta tensión se tramitan conforme a una normativa específica y mediante las reglas establecidas en las leyes sectoriales y la ley de procedimiento administrativo. Tras analizar los distintos tipos de procedimientos se concluye que la tramitación tiene correlación con una serie de conceptos: expediente, solicitud, proyecto, fase, trámite y tarea.

### Relación expediente, solicitud, proyecto, fase, trámite y tarea

Se tramita un solo expediente cada vez, que dispone de un número único (por mantener el historial el número usado no será el ID del expediente en la base de datos, si no un número paralelo generado desde un valor base tomado de otra base de datos existente). Cada expediente tiene un proyecto asociado. Un proyecto puede tener modificaciones siempre que no desvirtúen su esencia (finalidad). Cada expediente puede tener diferentes solicitudes (autorización administrativa previa, autorización administrativa de construcción, etc.) sobre el mismo proyecto (o el proyecto con uno o más modificados). Cada solicitud pasa por diferentes fases (ANÁLISIS SOLICITUD, INFORMACIÓN PÚBLICA, CONSULTAS, etc.) aunque hay casos en que puede haber más de una fase activa al mismo tiempo. Cada fase puede tener uno o más trámites (por ejemplo la fase de información pública puede tener el trámite de publicación en BOE y el trámite de publicación en BOP) y cada trámite puede tener una o más tareas (redactar anuncio, poner en firma, notificar, esperar plazo, etc.)

### Estructura de negocio de la tramitación

En nuestro caso queremos que la lógica de negocio no sea rígida, restringiendo lo que se puede o no se puede hacer en cada solicitud, fase, trámite, etc. de forma que no exista margen de maniobra para el usuario en tomar decisiones dentro de lo posible. Deseamos que la lógica sea definida de la siguiente forma:

1.  En cualquier estado o situación del expediente, es posible hacer cualquier cosa que no esté expresamente prohibida. En lugar de listar lo únicamente permitido, listar lo expresamente prohibido y permitir que se pueda hacer cualquier operación mientras no esté expresamente prohibida. Por ejemplo, una prohibición genérica sería que no se puede finalizar una fase si quedan trámites sin finalizar. Otra prohibición sería que no se puede iniciar la fase resolver si no se ha finalizado la fase análisis solicitud)
2.  Las prohibiciones que definen la lógica de la tramitación ha de obtenerse de valores definidos en tablas, no internamente escrito en el código. De esta forma la modificación de un precepto legal (y por tanto la lógica del procedimiento) no requiere modificar macros si no que solo requiere modificar los datos de las prohibiciones del procedimiento. Esto hace que el sistema se adapte rápidamente a los cambios.

Datos estructurales vs datos

### Lógica de Negocio - Enfoque basado en Motor de Reglas

#### Principio fundamental

La lógica de negocio de la aplicación **NO se implementa mediante código duro** (funciones, procedimientos almacenados, triggers con lógica específica). En su lugar, se basa en un **motor de reglas genérico** alimentado por tablas de configuración.

#### Características del sistema de reglas

1.  Las reglas viven en tablas, no en código

- - Toda la lógica de validación, restricción y flujo se almacena como **datos** en tablas específicas
  - Modificar el comportamiento del sistema implica modificar registros en estas tablas, no recompilar código
  - Las reglas son versionables, auditables y reversibles como cualquier otro dato

1.  Las reglas leen valores de tablas estructurales

- - El motor de reglas consulta dinámicamente los datos de las tablas de estructura básica (FASES, SOLICITUDES, EXPEDIENTES, PROYECTOS, etc.)
  - Las reglas evalúan condiciones basándose en:

<!-- -->

- - - Valores de campos específicos (ej: EXITO de una fase)
    - Existencia o ausencia de registros relacionados
    - Relaciones entre entidades
    - Contexto del expediente (tipo, instrumento ambiental, etc.)

1.  Las reglas producen acciones

> Las reglas pueden generar diferentes tipos de acciones:

- - **Bloquear**: Impedir al usuario realizar una acción (ej: crear una fase fuera de secuencia)
  - **Sugerir**: Mostrar advertencias o recomendaciones sin impedir la acción
  - **Obligar**: Forzar la creación/modificación de registros según condiciones
  - **Calcular**: Derivar valores automáticamente basándose en otros datos
  - **Validar**: Verificar la consistencia de los datos antes de confirmar cambios

1.  4\. Las reglas son editables sin tocar código

- - Los usuarios con permisos adecuados pueden modificar las reglas de negocio
  - No se requiere intervención de programadores para ajustar el comportamiento del sistema
  - Los cambios en las reglas tienen efecto inmediato
  - Esto permite adaptación ágil a cambios normativos o procedimentales

#### Implicaciones para el diseño actual

Fase de desarrollo/despliegue (Fases 1 y 2)

- **Sin restricciones activas**: El usuario tiene libertad total
- **Indicadores visuales**: La interfaz muestra advertencias informativas (no bloqueantes) sobre datos incompletos o inconsistentes
- **Educación progresiva**: Los usuarios se familiarizan con el "debería ser" antes de que se active el "debe ser"

Fase de producción con lógica activada (fases 3 y 4)

- **Restricciones automáticas**: El motor de reglas evalúa y aplica las reglas definidas
- **Flujos guiados**: El sistema sugiere o impone el siguiente paso según el contexto
- **Validación en tiempo real**: Se previenen inconsistencias antes de que se confirmen
- **Flexibilidad mantenida**: Ajustar una regla no requiere nueva versión de software

#### Principio de no redundancia

Los datos estructurales (como EXITO en FASES) **no duplican información** que pueda deducirse de otros datos. El motor de reglas es responsable de:

- Interpretar los datos básicos
- Aplicar las reglas configuradas
- Producir las acciones correspondientes

Los campos estructurales contienen **únicamente información primaria**, nunca derivada.

### El expediente y sus tipos

Los tipos de expedientes se definen en la tabla maestra TIPOS_EXPEDIENTES. Como se puede apreciar está asociado al tipo de titular de la instalación y tipo de uso de la misma. Digamos que es una clasificación de las distintas particularidades que tiene la legislación respecto a la tramitación en cada caso. El tipo de expediente define la lógica de la tramitación pues será una de las variables a tener en cuenta de cara a definir las restricciones o prohibiciones de la lógica de negocio.

El número de expediente NUMERO_AT es el **nexo que une todo** lo relativo a ese expediente.

El responsable ID es la persona que es responsable de ese expediente por completo y en la estructura empresarial es la única persona que está “permitida” (en el sentido que el sistema no impide a otro usuario actuar sobre ese expediente) a actuar sobre es expedientes y todas las tablas y datos asociadas.

El campo HEREDADO indica que ese expediente viene heredado del sistema de tramitación anterior. Esto indica que solo tendrá como datos en tablas lo que ya existe en el sistema anterior de control, pero no tendrá todas las tablas normales de un expediente moderno. De esta forma si este campo es SI, la lógica de negocio y el usuario están informados de porqué no hay datos en muchas tablas.

### La solicitud y sus tipos

Los tipos de solicitudes TIPO_SOLICITUD_ID están claramente definidas en la legislación y definen el resultado buscado por el solicitante. En cualquier caso siempre se pide un resultado de la misma desde el solicitante/peticionario/titular. Si no se obtiene el resultado esperado se produce una resolución de denegación, inadmisión, caducidad, aceptación renuncia, etc. para finalizar la solicitud. Una solicitud siempre (si no fuese así deberíamos plantearnos sacarla fuera de estos tipos de solicitudes) termina con una fase resolución. La situación en la que se encuentra una solicitud depende de lo que hayan concluido sus fases. Con macros se puede crear un “estado” como conjunción de los distintos estados de cada fase/trámite/tarea.

El campo FECHA es la fecha de la solicitud.

El campo PROYECTO_ID es la referencia al proyecto principal que se acompaña en la primera solicitud.

Hay tipos de solicitudes que se refieren a otras solicitudes que que hacen aquella se finalice. Estas son DESISTIMIENTO y RENUNCIA. EL parámetro que las une es el campo SOLICITUD_AFECTADA_ID que es NULL por defecto para cualquier resolución, pero con la lógica de negocio será obligatorio dar un valor eligiendo la solicitud que se renuncia o desiste.

### La fase y sus tipos

Hay diferentes tipos de fases, muchas de ellas son comunes a los distintos tipos de solicitudes. Los tipos de fases se definen en la tabla TIPOS_FASES. La característica principal de una fase es que tiene fechas de inicio y fin y que tiene un resultado de la misma. Una fase es un conjunto de trámites para obtener un requisito para alcanzar el objetivo de la solicitud. Por ejemplo obtención del pronunciamiento ambiental, de los condicionantes de los organismos, de la exposición del proyecto en información pública o de un informe favorable de un organismo externo.

Resumen de conceptos y flujo de trabajo con el diseño simplificado de fases.

Conceptos clave:

**Tabla FASES**: cada fase del expediente tiene campos clave:

- ID de fase, ID de solicitud, tipo de fase, fecha de inicio, fecha de fin, observaciones.
- Fecha de fin se define como la última fecha de finalización de todos los trámites asociados.
- EXITO: Es el valor booleano del resultado exitoso de la fase. Si es SI, la fase ha concluido exitosamente respecto a su tipo. Por ejemplo si la fase es INFORME MINISTERIO entonces se ha obtenido el informe favorable. Ese informe estará en el trámite/tarea correspondiente.
- DOCUMENTO_RESULTADO_ID: posible vínculo al documento oficial generado. Posiblemente desaparezca.

**Rellenado y flujo**:

- Al cerrar el último trámite asociado, se puede automatizar la fijación de la fecha fin de la fase.
- El éxito o no de la fase debe ser registrado manualmente por el usuario autorizado una vez analizada la documentación oficial correspondiente.
- Si EXITO es nulo, la fase está en curso o pendiente de cierre administrativo.
- Al tener el valor de éxito relleno (SI/NO) la fase se considera concluida y se puede permitir la creación o activación de fases sucesivas según reglas de negocio.

**Reglas de negocio y validación**:

- La fase sólo puede cerrarse tras completarse todos los trámites.
- La elección del resultado condiciona el flujo posterior y la posibilidad de nuevas fases.
- Campos automatizados (fecha fin) y campos manuales (éxito) coexistente para flexibilidad y control.
- Este diseño permite una gestión clara de la tramitación administrativa, manteniendo integridad, auditabilidad y control sobre el proceso mediante restricciones racionales y roles de usuario.

### El trámite y sus tipos

Los trámites son la capa de nuestro sistema con mayor variabilidad. Esto hace que necesitemos una estructura flexible pero coherente. La solución adoptada es la siguiente:

**Tablas necesarias**: para conseguir el objetivo

- Una tabla general de TIPOS_TRAMITES donde se listen todos los tipos y se incluya el nombre de la tabla asociada al tipo.
- Una tabla TRAMITES general que contenga los datos comunes a todos los tipos de trámites. Contiene instancias.
- Una tabla TRAMITES_XXXXXX por cada tipo con los campos específicos de ese tipo de trámite. Contiene instancias.

**Implicaciones de la solución adoptada**: consecuencias de la solución

- Hay una relación uno a uno entre el nombre de la tabla específica para un tipo de trámite y el tipo en si en la tabla TIPOS_TRAMITES. Si esa relación se rompe se emitiría un error.
- Las instancias en TRAMITES tienen que tener una instancia en la tabla de trámite especializado, correspondiente al valor del tipo de trámite.
- Existe el riesgo de instancias de trámites especializados huérfanos sin entrada en TRAMITES e instancias en TRAMITES sin su hijo correspondiente.

Estos riesgos se deben gobernar con dependencias en cascada y macros de comprobación. Esto no es una regla de la lógica de negocio, es un asunto de integridad referencial.

**Ventajas**: lo que nos ofrece****

- Integridad de datos fuerte
- Consultas SQL estándar
- Fácil validar datos específicos

**Desventajas**: lo que nos complica****

- Más tablas que mantener
- Requiere modificar BD al añadir nuevos tipos

**Estructura propuesta**: por confirmar

TIPOS_TRAMITES (tabla maestra)

 - ID

 - CODIGO

 - NOMBRE

 - DESCRIPCION

 - TABLA_EXTENSION (nombre de la tabla especializada, ej: "TRAMITES_REQUERIMIENTO")

TRAMITES (tabla base)

 - ID

 - FASE_ID (FK → FASES)

 - TIPO_TRAMITE_ID (FK → TIPOS_TRAMITES)

 - FECHA_INICIO

 - FECHA_FIN

 - OBSERVACIONES

TRAMITES\_\[TIPO_ESPECIFICO\] (una tabla por cada tipo)

 - TRAMITE_ID (PK + FK → TRAMITES, relación 1:1)

 - \[campos específicos del tipo de trámite\]
