
# IMDB Scraper - Scraping con Manejo de Proxies y Almacenamiento en PostgreSQL

Este proyecto realiza el scraping de las 50 mejores películas desde IMDb, guardando los datos en una base de datos PostgreSQL y exportando también a CSV (llamado imdb_top_50.csv), y que se usa para crear la bd relacional con postgres. Incluye funciones de análisis SQL avanzado y mecanismos de tolerancia a fallos mediante proxies y red Tor.

---

## Manejo de IPs, proxies y resolución de bloqueos de IMDb

Durante las primeras etapas del desarrollo de este scraper, aparecían varias problemas: el sitio web de IMDb no cargaba correctamente cuando se realizaban solicitudes desde una dirección IP ubicada en **Colombia**.

### Detección del problema

Al hacer peticiones `GET` con herramientas básicas como `requests` y `curl`, la respuesta HTML tenía código `200 OK`, pero **no contenía información valiosa** para el scraping. En concreto, elementos clave como el bloque `<script type="application/ld+json">`, que contiene los datos estructurados de las películas, **no aparecían** en la respuesta.

Esto indicaba  que **IMDb estaba aplicando un bloqueo geográfico o por IP**, impidiendo el acceso  desde ciertas regiones.

### Verificación con VPN

Para comprobar si otras direcciones IP funcionaban correctamente, se utilizó **ProtonVPN** y se establecieron conexiones con servidores en **Europa y Estados Unidos**. Desde estas ubicaciones, el scraping funcionó sin inconvenientes: el contenido completo del sitio se cargaba, incluyendo los datos necesarios para parsear las películas.

Esto confirmó que el scraper **no fallaba por lógica o errores de código**, sino por un **bloqueo impuesto por IMDb según la IP de origen**.

---

##  Estrategias implementadas para superar el bloqueo

### 1.  Proxies públicas gratuitas

Se probaron más de **2000 proxies gratuitos**, obtenidos de listas online. Sin embargo, esta estrategia no tuvo éxito. Los proxies:
- Estaban fuera de servicio,
- Eran excesivamente lentos,
- También estaban bloqueados por IMDb.

### 2.  Dockerizando conexiones VPN (OpenVPN y WireGuard)

Se intentó montar conexiones VPN dentro de contenedores Docker utilizando configuraciones `.ovpn` (OpenVPN) y `.conf` (WireGuard). El objetivo era automatizar la rotación de IPs sin depender de software externo.

Aunque los contenedores se levantaban correctamente, surgieron **problemas de red internos**:
- Los contenedores no podían establecer correctamente los túneles VPN.
- Era necesario manipular adaptadores de red o privilegios del host para enrutar el tráfico, lo cual comprometía la portabilidad y seguridad del entorno.

Por estas razones, esta alternativa fue descartada.

---

## Solución final: uso de la red Tor con proxy SOCKS5

Como última estrategia, se optó por integrar **Tor** al scraper. Tor permite enrutar el tráfico a través de una red global de nodos, ocultando la IP original del cliente.

Se configuró un **proxy SOCKS5** local (`socks5h://127.0.0.1:9150`) y se redireccionaron todas las solicitudes HTTP y HTTPS del scraper a través de esta red y extrae la informacion para guardarala en el archivo imdb_top_50.csv que se guarda en data.

###  Implementación técnica

- Se creó un módulo llamado `retry.py` con un sistema de **reintentos automáticos**.
- Antes de cada request importante, se hace una solicitud a `http://httpbin.org/ip` para registrar la IP actual de salida.
- Si el contenido retornado por IMDb no es válido (por ejemplo, si falta el bloque de películas), se **reintenta automáticamente** después de una pausa exponencial.

Este mecanismo permite que el scraper **siga intentando con nuevas IPs proporcionadas por Tor**, hasta encontrar una que no esté bloqueada por IMDb.

###  Ventajas

- No requiere servicios externos de pago.
- Funciona de forma local con mínima configuración.
- Es confiable y suficientemente anónimo para scraping ocasional.
---
### Desventajas
- Se requiere el navegador instalado y abierto para usar el puerto 9150.

## Resultado

Gracias al uso de la red Tor con rotación de IPs, el scraper ahora puede acceder de forma estable a los datos de IMDb, incluso desde regiones con restricciones como Colombia. Este sistema es tolerante a fallos, registra cada intento y ofrece la capacidad de recuperación automática ante bloqueos temporales.
Sin embargo, se recomienda considerar el uso de proxies de pago en entornos de producción, ya que su configuración es mucho más sencilla y, en despliegues en la nube, no requieren la instalación adicional de servicios como Tor, lo cual simplifica la arquitectura y mejora la mantenibilidad del sistema.

"""
# Guardar la sección completa de PostgreSQL y consultas como un bloque listo para README.md

### Uso de PostgreSQL para almacenamiento y análisis

Además del scraping de IMDb, el sistema cuenta con una base de datos PostgreSQL que se **levanta desde un contenedor Docker**. Esta base de datos actúa como almacenamiento principal de la información obtenida, y es usada también para realizar consultas avanzadas sobre las películas extraídas.

### Estructura de la base de datos

Por otra parte, una vez levantado el contenedor de posrtgres, se crea una base de datos llamada por defecto `imdb_db`, con dos tablas principales:

- `peliculas`: almacena título, año, calificación, duración y metascore.
- `actores`: almacena los actores principales asociados a cada película.

Estas tablas se crean y gestionan automáticamente desde los scripts del proyecto al ejecutar `main.py`.

---

###  Consultas SQL realizadas

Una vez que los datos se guardan en la base de datos, se ejecutan automáticamente una serie de **consultas avanzadas** que permiten analizar el contenido extraído. Estas consultas están almacenadas en el archivo `advanced_queries.sql` en db.


Para lenvantar la bd se usa el comando docker-compose up --build -d    y si se desea ingresar a la bd por terminal se puede hacer con el comando docker exec -it postgres_db psql -U imdb_user -d imdb_db    y luego aplicar las consultas de  `advanced_queries.sql` para obtener la info, o cargando la bd con el complemento de database en vscode y usando la info de la bd que está en el archivo docker-compose. 

### Flujo para cargar y ejecutar.
- Primero se debe crear enterno de python. 
- luego instalar el requirement.txt.
- Posteriomente levantar la bd de postgres con docker-compose up -build -d. 
- Posteriomente abrir TOR. 
- y Desde el entorno activo ejecutar main.py

### Comparación Técnica: Implementación alternativa con Selenium o Playwright

Aunque el scraper actual fue construido utilizando `requests`, `BeautifulSoup` y manejo de proxies con Tor, en escenarios más complejos podría ser beneficioso usar herramientas como **Selenium** o **Playwright**, especialmente cuando se necesita interactuar con contenido generado por JavaScript o superar bloqueos automáticos más sofisticados.

---
### Cómo se implementaría con Playwright o Selenium

#### Configuración avanzada del navegador
- Inicialmente para evitar problemas de consumo de memoria activar el **Modo headless o invisible**.
- Personalización de **user-agent**, idioma, tamaño de pantalla, y otros headers.
- Técnicas de **evasión de detección WebDriver**:
- En Selenium: deshabilitar extensiones, ocultar variables como `navigator.webdriver`.
- En Playwright: viene con evasión por defecto en muchos escenarios.
-  Se busca en el html los frames espeficicos y si  la informacion esta anidada, para extraerla. 
---
#### Selectores dinámicos y esperas explícitas
- Uso de métodos como `WebDriverWait` (Selenium) o `page.wait_for_selector` (Playwright), permite interactuar con elementos que cargan asíncronamente (desplegables, modales, etc.),  esto mejora la robustez del scraper ante cambios en la estructura DOM.
---
#### Manejo de CAPTCHA o JavaScript rendering
- Herramientas como Playwright permiten **capturar captchas**, tomar capturas de pantalla o resolver ciertos retos visuales mediante servicios externos como 2catpcha, ademas el Javascript Rendering es ultil en escenarios donde la información no está en el HTML inicial.
--
#### Control de concurrencia (workers / colas)
- Se puede lanzar múltiples instancias del navegador en paralelo usando asyncio en  playwright y ThreadPoolExecutor  o  multiprocessing en Selenium, esto permite scrapear múltiples páginas al mismo tiempo, mejorando los tiempos de los procesos.

---
###  ¿Por qué no usar Scrapy?

**Scrapy** es un herramienta que funciona bastante bien, con sitios con HTML estático o estructurado de forma consistente, pero tiene limitaciones como:
- No renderiza JavaScript nativamente (se requiere de integración con Playwright para superar este problema).
- Menor control directo sobre navegación dinámica o acciones del navegador (scrolls, clicks, etc.).
