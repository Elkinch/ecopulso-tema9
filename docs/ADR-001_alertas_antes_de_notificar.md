# ADR-001: Guardar la alerta antes de notificar

- **Estado:** Propuesta (validar en el debate).
- **Requisito no funcional vinculado:** RNF-1 (resiliencia de alertas).
- **Contenedores afectados:** Servicio de alertas, Base de datos.

## Contexto
El servicio de correo es un sistema externo y puede no estar disponible. Una alerta que solo existe como correo se pierde si el envío falla.

## Decisión
Toda alerta se guarda primero en la base de datos con estado `pendiente`. El Servicio de alertas intenta enviarla y actualiza el estado. Si falla, reintenta con espera creciente (1, 5 y 15 minutos, cuatro intentos en total). Agotados los intentos pasa a `fallida`. En todos los estados la alerta es visible en el panel.

## Alternativas descartadas
1. **Enviar y descartar si falla:** se pierden alertas.
2. **Bloquear la carga de lecturas hasta que el correo responda:** acopla el flujo principal a un servicio externo.
3. **Broker de mensajes externo:** excesivo para el MVP y añade un servicio que operar.

## Consecuencias
- (+) La alerta no se pierde y el panel no depende del correo.
- (+) Se puede probar con un doble de correo (ver `prototipo/`).
- (−) Más estados y lógica de reintentos; el aviso puede llegar con retraso.
- (−) Posible envío duplicado si falla la confirmación; se mitiga con un identificador estable por alerta (misma lectura y regla, misma alerta).

## Evidencia
`prototipo/test_alerts.py` (7 pruebas) y `prototipo/salida_demo.txt`.
