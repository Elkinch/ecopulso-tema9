"""EcoPulso - prototipo de ADR-001: la alerta se guarda ANTES de notificar.

Solo usa la biblioteca estandar de Python. Datos sinteticos. Sin servicios externos.
"""
import hashlib
import sqlite3
from datetime import datetime, timedelta

# Espera antes de cada reintento (minutos). Cuatro intentos en total; luego "fallida".
BACKOFF_MIN = (1, 5, 15)


class MailUnavailable(Exception):
    """El servicio de correo (externo) no responde."""


class FakeMailer:
    """Doble de prueba del servicio de correo. 'up' permite simular su caida."""

    def __init__(self):
        self.up = True
        self.sent = []

    def send(self, to, subject, body):
        if not self.up:
            raise MailUnavailable("servicio de correo no disponible")
        self.sent.append((to, subject, body))


SCHEMA = """
CREATE TABLE IF NOT EXISTS alerts (
  id TEXT PRIMARY KEY,
  space TEXT NOT NULL,
  explanation TEXT NOT NULL,
  recipient TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pendiente', 'enviada', 'fallida')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_attempt_at TEXT NOT NULL,
  last_error TEXT,
  created_at TEXT NOT NULL
)
"""


def _iso(dt):
    return dt.isoformat(timespec="seconds")


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def alert_id(space, day, rule):
    """Identificador estable: la misma lectura y regla no genera dos alertas."""
    return hashlib.sha1(f"{space}|{day}|{rule}".encode()).hexdigest()[:12]


def evaluate_reading(conn, space, day, value, unit, threshold, recipient, now):
    """Evalua una lectura. Si supera el umbral, guarda la alerta como 'pendiente'.

    Nunca llama al servicio de correo: la lectura se procesa aunque el correo este caido.
    Devuelve el id de la alerta, o None si no supera el umbral.
    """
    if value <= threshold:
        return None
    rule = f"umbral {threshold} {unit}"
    aid = alert_id(space, day, rule)
    explanation = (f"{space}: consumo de {value} {unit} el {day} supera el umbral "
                   f"de {threshold} {unit} (regla: {rule}).")
    conn.execute(
        "INSERT OR IGNORE INTO alerts (id, space, explanation, recipient, status, attempts,"
        " next_attempt_at, last_error, created_at) VALUES (?, ?, ?, ?, 'pendiente', 0, ?, NULL, ?)",
        (aid, space, explanation, recipient, _iso(now), _iso(now)),
    )
    conn.commit()
    return aid


def dispatch_pending(conn, mailer, now):
    """Intenta enviar las alertas pendientes cuya hora de reintento ya llego."""
    rows = conn.execute(
        "SELECT * FROM alerts WHERE status = 'pendiente' AND next_attempt_at <= ? ORDER BY created_at, id",
        (_iso(now),),
    ).fetchall()
    result = {"enviadas": 0, "reintentos": 0, "fallidas": 0}
    for r in rows:
        try:
            mailer.send(r["recipient"], f"Alerta de consumo: {r['space']}", r["explanation"])
        except MailUnavailable as exc:
            attempts = r["attempts"] + 1
            if attempts > len(BACKOFF_MIN):
                conn.execute("UPDATE alerts SET status='fallida', attempts=?, last_error=? WHERE id=?",
                             (attempts, str(exc), r["id"]))
                result["fallidas"] += 1
            else:
                nxt = now + timedelta(minutes=BACKOFF_MIN[attempts - 1])
                conn.execute("UPDATE alerts SET attempts=?, next_attempt_at=?, last_error=? WHERE id=?",
                             (attempts, _iso(nxt), str(exc), r["id"]))
                result["reintentos"] += 1
        else:
            conn.execute("UPDATE alerts SET status='enviada', last_error=NULL WHERE id=?", (r["id"],))
            result["enviadas"] += 1
    conn.commit()
    return result


def list_alerts(conn):
    """Lo que muestra el panel: TODAS las alertas, con su estado de envio."""
    return [dict(r) for r in conn.execute("SELECT * FROM alerts ORDER BY created_at, id")]
