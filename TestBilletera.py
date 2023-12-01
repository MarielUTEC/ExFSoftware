import unittest
from flask import Flask
from flask.testing import FlaskClient
from Examen import app, BD

class TestBilletera(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Caso de prueba exitoso: Obtener contactos
    def test_obtener_contactos_exitoso(self):
        response = self.app.get('/billetera/contactos?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertIn('123', response.json)

    # Caso de prueba exitoso: Realizar pago
    def test_realizar_pago_exitoso(self):
        response = self.app.post('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mensaje'], 'Transacción exitosa')

    # Caso de prueba de error: Número de cuenta incorrecto al obtener contactos
    def test_obtener_contactos_error_cuenta_incorrecto(self):
        response = self.app.get('/billetera/contactos?minumero=99999')
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)
        self.assertEqual(response.json['mensaje'], 'Número de cuenta incorrecto')

    # Caso de prueba de error: Saldo insuficiente al realizar pago
    def test_realizar_pago_error_saldo_insuficiente(self):
        response = self.app.post('/billetera/pagar?minumero=123&numerodestino=456&valor=500')
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)
        self.assertEqual(response.json['mensaje'], 'Saldo insuficiente para realizar la transacción')

    # Caso de prueba de error: Destino no está en la lista de contactos
    def test_realizar_pago_error_destino_no_en_contactos(self):
        response = self.app.post('/billetera/pagar?minumero=21345&numerodestino=789&valor=50')
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)
        self.assertEqual(response.json['mensaje'], 'El destino no está en la lista de contactos')


if __name__ == '__main__':
    unittest.main()
