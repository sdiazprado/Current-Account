Generador de Boletín de Organismos Internacionales 
Este ecosistema automatizado, desarrollado en Python 3.12, permite la extracción, filtrado y consolidación de información clave (discursos, reportes y working papers) de las principales instituciones financieras del mundo. El objetivo es estandarizar la vigilancia macroeconómica y reducir en un 90% el tiempo de recolección manual de datos.

Capacidades Principales
Extracción Multi-Fuente: Conexión directa con las bases de datos de:

FMI: Uso de Coveo API para búsqueda unificada.

BPI (BIS): Triple validación de discursos (JSON + HTML Meta-tags).

FEM (World Economic Forum): Integración con Apollo API.

Banco Mundial & FSB: Scraping dinámico de publicaciones y comunicados.

Filtros de Precisión: Sistema de validación de fechas por descripción de contenido para evitar "rezagados" de meses anteriores.

Exportación Institucional: Generación automática de documentos .docx con estilos, jerarquías y formatos listos para distribución oficial.

🛠️ Arquitectura del Proyecto
El proyecto sigue una estructura modular para facilitar el mantenimiento de los scrapers individuales:

Plaintext

├── app1.py              # Dashboard principal (Streamlit)
├── core_logic.py        # Procesamiento de fechas y orquestación de datos
├── scrapers/            # Módulos de extracción por organismo
│   ├── fmi_coveo.py     # Integración API FMI
│   ├── bis_logic.py     # Filtros avanzados para el BPI
│   └── wef_apollo.py    # Conexión con el Foro Económico Mundial
├── reports_gen.py       # Motor de formateo python-docx
├── requirements.txt     # Dependencias (Streamlit, BeautifulSoup, etc.)
└── README.md            # Documentación técnica
💻 Stack Tecnológico
Lenguaje: Python 3.12+

Interfaz: Streamlit (v1.32+)

Análisis Web: BeautifulSoup4, Requests (Sessions), Selenium.

Procesamiento de Datos: Pandas, Python-dateutil.

Documentación: Python-docx (con manejo de tablas y estilos).

⚙️ Instalación en Entornos Restringidos
Para correr este proyecto en equipos con restricciones de red o múltiples versiones de Python (como entornos de banca central), se recomienda el uso de Rutas Absolutas:

Instalación de dependencias:

DOS

C:\Ruta\A\Tu\Python312\python.exe -m pip install -r requirements.txt
Ejecución de la aplicación:

DOS

C:\Ruta\A\Tu\Python312\python.exe -m streamlit run app1.py
📖 Flujo de Uso
Configuración: Seleccionar el rango de fechas (mes/año) y los organismos de interés en la barra lateral.

Barrido Dinámico: La aplicación consulta las APIs y realiza el filtrado de metadatos en tiempo real.

Previsualización: Revisar la tabla de resultados para verificar links y títulos detectados.

Generación: Clic en "Generar Boletín" para compilar toda la información en un archivo Word listo para descargar.
