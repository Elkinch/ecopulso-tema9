"""Demostracion de ADR-001 para el video (3 a 4 min). Ejecutar: python demo.py"""
from datetime import datetime, timedelta

import alerts as a

now = datetime(2026, 11, 4, 9, 0, 0)
conn, mail = a.connect(), a.FakeMailer()


def panel(titulo):
    print(f"\n--- PANEL: {titulo} ---")
    for x in a.list_alerts(conn):
        print(f"  [{x['status'].upper():9}] intentos={x['attempts']} | {x['explanation']}")


print("1) El servicio de correo se apaga (se simula la caida).")
mail.up = False
print("2) Llega una lectura de 120 kWh en Lab 1 (umbral 100 kWh).")
a.evaluate_reading(conn, "Lab 1", "2026-11-03", 120, "kWh", 100, "responsable@ejemplo.test", now)
print("   La lectura se procesa aunque el correo este caido.")
print("3) El servicio de alertas intenta enviar:", a.dispatch_pending(conn, mail, now))
panel("la alerta NO se perdio; esta pendiente y visible")

print("\n4) Primer reintento (1 min despues), el correo sigue caido:")
print("  ", a.dispatch_pending(conn, mail, now + timedelta(minutes=1)))
panel("sigue pendiente; proximo reintento en 5 min")

print("\n5) El servicio de correo se recupera.")
mail.up = True
print("6) Reintento programado (6 min despues):", a.dispatch_pending(conn, mail, now + timedelta(minutes=6)))
panel("alerta enviada")
print(f"\nCorreos entregados: {len(mail.sent)}")
