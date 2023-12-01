# Desarrollar un software que implemente una billetera electrónica para Celular, al estilo de Yape o Plin
# Se debe soportar las operaciones:

#-	Contactos: Lista los contactos de un número de teléfono con sus nombres.
#-	Pagar: Transfiere un valor a otro número (debe ser un contacto). La cuenta debe tener saldo suficiente para hacer la transferencia.
#-	Historial: Muestra el saldo y la lista de operaciones, tanto de envío como de recepción de dinero.

# O sea como una clase Cuenta que tenga de atributos a Numero, Saldo, Contactos:String[], historial(), pagar(destino,valor) 
# Tambien una Clase Operacion que tenga de atributos a NumeroDestino, Fecha, Valor
# Que estas 2 clases esten conectadas asi: Cuenta realiza n Operaciones

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class Operacion:
    def __init__(self, numero_destino, valor, fecha=None):
        self.numero_destino = numero_destino
        self.fecha = fecha or datetime.now()
        self.valor = valor

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos=None):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos or {}
        self.historial_operaciones = []

    def agregar_contacto(self, numero_contacto, nombre_contacto):
        self.contactos[numero_contacto] = nombre_contacto

    def listar_contactos(self):
        return self.contactos

    def pagar(self, destino, valor):
        if destino in self.contactos:
            if self.saldo >= valor:
                self.saldo -= valor
                operacion = Operacion(destino, valor)
                self.historial_operaciones.append(operacion)
                return {"mensaje": "Transacción exitosa", "nuevo_saldo": self.saldo, "fecha": operacion.fecha}
            else:
                return {"mensaje": "Saldo insuficiente para realizar la transacción"}
        else:
            return {"mensaje": "El destino no está en la lista de contactos"}

    def historial(self):
        saldo_str = f"Saldo de {self.nombre}: {self.saldo} Operaciones de {self.nombre}:  "
        for operacion in self.historial_operaciones:
            if operacion.valor > 0:
                saldo_str += f"- Pago recibido de {operacion.valor} de {self.contactos.get(operacion.numero_destino, 'Desconocido')}\n"
            else:
                saldo_str += f"- Pago realizado de {-operacion.valor} a {self.contactos.get(operacion.numero_destino, 'Desconocido')}\n"
        return {"historial": saldo_str}

# Inicializamos la aplicación con un conjunto de cuentas y contactos
BD = [
    Cuenta("21345", "Arnaldo", 200, {"123": "Luisa", "456": "Andrea"}),
    Cuenta("123", "Luisa", 400, {"456": "Andrea"}),
    Cuenta("456", "Andrea", 300, {"21345": "Arnaldo"})
]

# Definimos los endpoints
@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    minumero = request.args.get('minumero')
    cuenta = next((c for c in BD if c.numero == minumero), None)
    if cuenta:
        return jsonify(cuenta.listar_contactos())
    else:
        return jsonify({"mensaje": "Número de cuenta incorrecto"})

@app.route('/billetera/pagar', methods=['POST'])
def realizar_pago():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))

    cuenta = next((c for c in BD if c.numero == minumero), None)
    if cuenta:
        resultado_pago = cuenta.pagar(numerodestino, valor)
        return jsonify(resultado_pago)
    else:
        return jsonify({"mensaje": "Número de cuenta incorrecto"})

@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    minumero = request.args.get('minumero')
    cuenta = next((c for c in BD if c.numero == minumero), None)
    if cuenta:
        historial = cuenta.historial()
        return jsonify(historial)
    else:
        return jsonify({"mensaje": "Número de cuenta incorrecto"})

# Ejecutamos la aplicación en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000)
