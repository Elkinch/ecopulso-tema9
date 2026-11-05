# Bitácora de IA

> Borrador asistido por IA. El equipo debe completar los campos `[Completar]` con lo que realmente comprobó y decidió. Si no se usa IA, declararlo y analizar una sugerencia hipotética que requeriría verificación.

## Entrada 1: caso y borrador de diagramas
- **Objetivo:** elegir el caso y proponer contexto y contenedores.
- **Herramienta:** Claude (Anthropic), chat.
- **Propuesta (fragmento):** "Usar EcoPulso; contenedores: aplicación web, API, motor de alertas y base de datos; el importador CSV puede ser parte de la API o un proceso aparte."
- **Comprobación:** contrastar con las evidencias mínimas del tema y con el Proyecto 5; revisar que no mezcle C4 con despliegue. Resultado: [Completar]
- **Errores detectados:** [Completar]
- **Decisión humana:** se adopta EcoPulso; el importador queda como componente de la API. [Confirmar]

## Entrada 2: ADR-001 y RNF
- **Objetivo:** redactar la decisión de arquitectura y el requisito vinculado.
- **Herramienta:** Claude (Anthropic), chat.
- **Propuesta (fragmento):** "Guardar la alerta como pendiente y reintentar; RNF: 100 % de alertas visibles si el correo cae."
- **Comprobación:** que el RNF sea medible, que exista prueba con correo caído y que se hayan evaluado alternativas. Resultado: [Completar]
- **Errores detectados:** [Completar]
- **Decisión humana:** se acepta; se añaden el estado `fallida` y un identificador estable por alerta contra duplicados. [Confirmar]

## Entrada 3: fuentes
- **Objetivo:** proponer fuentes pertinentes.
- **Herramienta:** Claude (Anthropic), chat, sin acceso a búsqueda.
- **Propuesta:** lista de seis fuentes con autor, año y enlace.
- **Comprobación:** la IA puede inventar o alterar citas; abrir cada enlace y comprobar autor, título y fecha. Resultado: [Completar]
- **Decisión humana:** incluir solo fuentes verificadas. [Registrar resultado]

## Entrada 4: prototipo de ADR-001
- **Objetivo:** demostrar el comportamiento de ADR-001 con código ejecutable.
- **Herramienta:** Claude (Anthropic), chat con ejecución de código.
- **Propuesta:** `prototipo/alerts.py`, `test_alerts.py` y `demo.py` (Python estándar, SQLite, doble de correo).
- **Comprobación:** al prepararlo se ejecutaron las 7 pruebas y pasaron, y se ejecutó `demo.py` (salida en `prototipo/salida_demo.txt`). El equipo debe volver a ejecutarlas en su equipo y revisar que las pruebas cubran RNF-1. Resultado: el equipo ejecutó las 7 pruebas y `demo.py` en Windows y todo pasó (captura en `docs/evidencias/captura_pruebas_y_demo_windows.png`). Falta revisar que las pruebas cubran RNF-1. [Confirmar]
- **Errores detectados:** [Completar]
- **Decisión humana:** [Completar]
