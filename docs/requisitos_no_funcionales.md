# Requisitos no funcionales verificables

| ID | Requisito | Criterio verificable | Cómo se verifica |
|---|---|---|---|
| RNF-1 | Resiliencia de alertas | Con el correo caído, el 100 % de las alertas generadas queda visible como "pendiente" y se envía al recuperarse. | Prueba automática con doble de correo (`prototipo/test_alerts.py`). |
| RNF-2 | Accesibilidad básica | Panel operable solo con teclado; contraste de texto mínimo 4,5:1; cada gráfico tiene una tabla de datos equivalente. | Lista de verificación basada en WCAG 2.2 y Lighthouse o axe. |
| RNF-3 | Control de acceso | Solo el responsable de espacio carga lecturas y cambia umbrales; el estudiante solo consulta. | Pruebas de API: el rol estudiante recibe 403. |
| RNF-4 | Manejo de errores | Un CSV inválido devuelve informe por fila (línea y motivo), sin guardado parcial y sin trazas internas. | Pruebas con CSV de negativos, duplicados y fechas inválidas. |

**Estado de verificación:** solo RNF-1 tiene prueba ejecutable en este paquete. RNF-2, RNF-3 y RNF-4 corresponden a la API y la aplicación web, que no se construyen en este tema; quedan como criterios a verificar cuando existan.
