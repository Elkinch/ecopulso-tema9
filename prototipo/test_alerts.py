"""Pruebas de aceptacion de ADR-001 y RNF-1. Ejecutar: python -m unittest -v"""
import unittest
from datetime import datetime, timedelta

import alerts as a

T0 = datetime(2026, 11, 4, 9, 0, 0)


def nuevo():
    return a.connect(), a.FakeMailer()


def lectura(conn, space="Lab 1", day="2026-11-03", value=120, thr=100, now=T0):
    return a.evaluate_reading(conn, space, day, value, "kWh", thr, "responsable@ejemplo.test", now)


class TestAdr001(unittest.TestCase):
    def test_no_hay_alerta_bajo_el_umbral(self):
        conn, _ = nuevo()
        self.assertIsNone(lectura(conn, value=90))
        self.assertEqual(a.list_alerts(conn), [])

    def test_alerta_visible_como_pendiente_con_el_correo_caido(self):  # RNF-1
        conn, mail = nuevo()
        mail.up = False
        lectura(conn)
        a.dispatch_pending(conn, mail, T0)
        lst = a.list_alerts(conn)
        self.assertEqual(len(lst), 1)
        self.assertEqual(lst[0]["status"], "pendiente")
        self.assertIn("supera el umbral", lst[0]["explanation"])
        self.assertEqual(mail.sent, [])

    def test_se_envia_al_recuperarse_el_correo(self):  # RNF-1
        conn, mail = nuevo()
        mail.up = False
        lectura(conn)
        a.dispatch_pending(conn, mail, T0)
        mail.up = True
        res = a.dispatch_pending(conn, mail, T0 + timedelta(minutes=1))
        self.assertEqual(res["enviadas"], 1)
        self.assertEqual(a.list_alerts(conn)[0]["status"], "enviada")
        self.assertEqual(len(mail.sent), 1)

    def test_no_reintenta_antes_de_la_hora_programada(self):
        conn, mail = nuevo()
        mail.up = False
        lectura(conn)
        a.dispatch_pending(conn, mail, T0)  # primer fallo: reintento en 1 min
        mail.up = True
        a.dispatch_pending(conn, mail, T0 + timedelta(seconds=30))
        self.assertEqual(mail.sent, [])
        self.assertEqual(a.list_alerts(conn)[0]["status"], "pendiente")

    def test_pasa_a_fallida_tras_agotar_los_intentos_y_sigue_visible(self):
        conn, mail = nuevo()
        mail.up = False
        lectura(conn)
        now = T0
        for espera in (0, 1, 5, 15):  # 4 intentos en total
            a.dispatch_pending(conn, mail, now + timedelta(minutes=espera))
            now = now + timedelta(minutes=espera)
        alerta = a.list_alerts(conn)[0]
        self.assertEqual(alerta["status"], "fallida")
        self.assertEqual(alerta["attempts"], 4)
        self.assertEqual(len(a.list_alerts(conn)), 1)

    def test_la_misma_lectura_no_genera_alertas_ni_correos_duplicados(self):
        conn, mail = nuevo()
        lectura(conn)
        lectura(conn)
        self.assertEqual(len(a.list_alerts(conn)), 1)
        a.dispatch_pending(conn, mail, T0)
        a.dispatch_pending(conn, mail, T0 + timedelta(minutes=30))
        self.assertEqual(len(mail.sent), 1)

    def test_el_100_por_ciento_de_las_alertas_queda_visible(self):  # RNF-1
        conn, mail = nuevo()
        mail.up = False
        for i in range(25):
            lectura(conn, space=f"Aula {i}", value=150)
        a.dispatch_pending(conn, mail, T0)
        lst = a.list_alerts(conn)
        self.assertEqual(len(lst), 25)
        self.assertTrue(all(x["status"] == "pendiente" for x in lst))


if __name__ == "__main__":
    unittest.main()
