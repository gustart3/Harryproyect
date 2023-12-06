import mysql.connector
import math


from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
#from flask import CORS

app = Flask(__name__)
#CORS(app)




# Código de tu base de datos y lógica de manejo de datos

print("\033[H\033[J")  # Limpiar la consola

class Casas:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Casas(
            codigo INT PRIMARY KEY,
            casa VARCHAR(255) NOT NULL,
            atributo_1 VARCHAR(255) NOT NULL,               
            atributo_2 VARCHAR(255) NOT NULL, 
            atributo_3 VARCHAR(255) NOT NULL, 
            atributo_4 VARCHAR(255) NOT NULL, 
            atributo_5 VARCHAR(255) NOT NULL, 
            atributo_6 VARCHAR(255) NOT NULL,
            atributo_7 VARCHAR(255) NOT NULL, 
            atributo_8 VARCHAR(255) NOT NULL,
            atributo_9 VARCHAR(255) NOT NULL                                                   
            )
        ''')
        self.conn.commit()

    # AGREGAR LAS CASAS
    def crear_casa(self, codigo, casa, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9):
        try:
            self.cursor.execute(f"SELECT * FROM Casas WHERE codigo = {codigo}")
            casa_exist = self.cursor.fetchone()
            if casa_exist:
                return False

            sql = f"INSERT INTO Casas \
                   (codigo, casa, atributo_1, atributo_2, atributo_3,atributo_4,atributo_5,atributo_6,atributo_7, atributo_8, atributo_9) \
                   VALUES \
                   ({codigo}, '{casa}', '{atributo_1}', '{atributo_2}', '{atributo_3}', '{atributo_4}', '{atributo_5}', '{atributo_6}', '{atributo_7}', '{atributo_8}', '{atributo_9}')"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("Error al agregar casa:")
            print(f"Error code: {err.errno}")
            print(f"SQL State: {err.sqlstate}")
            print(f"Mensaje: {err.msg}")
            return False

    # Listar casas
    def listar_casas(self):
        try:
            self.cursor.execute("SELECT * FROM Casas")
            casas = self.cursor.fetchall()
            print("-" * 30)
            for casa in casas:
                print(f"Codigo.......: {casa['codigo']}")
                print(f"Casa.........: {casa['casa']}")
                print(f"Atributo 1...: {casa['atributo_1']}")
                print(f"Atributo 2...: {casa['atributo_2']}")
                print(f"Atributo 3...: {casa['atributo_3']}")
                print(f"Atributo 4...: {casa['atributo_4']}")
                print(f"Atributo 5...: {casa['atributo_5']}")
                print(f"Atributo 6...: {casa['atributo_6']}")
                print(f"Atributo 7...: {casa['atributo_7']}")
                print(f"Atributo 8...: {casa['atributo_8']}")
                print(f"Atributo 9...: {casa['atributo_9']}")
                print("-" * 30)
        except mysql.connector.Error as err:
            print(f"Error al listar casas: {err}")

    # Consultar casa
    def consultar_casa(self, codigo):
        try:
            self.cursor.execute(f"SELECT * FROM Casas WHERE codigo = {codigo}")
            casa_exist = self.cursor.fetchone()
            if casa_exist:
                return casa_exist
        except mysql.connector.Error as err:
            print(f"Error al consultar casa: {err}")

class Estudiantes:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Estudiantes(
            codigo_identificacion INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            edad INT NOT NULL,
            sexo VARCHAR(1) NOT NULL,
            atributo_1 VARCHAR(255) NOT NULL,               
            atributo_2 VARCHAR(255) NOT NULL, 
            atributo_3 VARCHAR(255) NOT NULL, 
            atributo_4 VARCHAR(255) NOT NULL, 
            atributo_5 VARCHAR(255) NOT NULL, 
            atributo_6 VARCHAR(255) NOT NULL,
            atributo_7 VARCHAR(255) NOT NULL, 
            atributo_8 VARCHAR(255) NOT NULL,
            atributo_9 VARCHAR(255) NOT NULL,
            casa_asignada INT,  
            curso_asignado INT NOT NULL,
            FOREIGN KEY (casa_asignada) REFERENCES Casas(codigo) 
            )''')
        self.conn.commit()

    def listar_estudiantes(self):
        try:
            self.cursor.execute("SELECT Estudiantes.*, Casas.casa AS nombre_casa FROM Estudiantes JOIN Casas ON Estudiantes.casa_asignada = Casas.codigo")
            estudiantes = self.cursor.fetchall()
            print("-" * 30)
            for estudiante in estudiantes:
                # Imprimir los detalles del estudiante
                print(f"Codigo Identificacion: {estudiante['codigo_identificacion']}")
                print(f"Nombre: {estudiante['nombre']}")
                print(f"Apellido: {estudiante['apellido']}")
                print(f"Casa Asignada: {estudiante['casa_asignada']}")
                print("-" * 30)
            
            # Retornar la lista de estudiantes
            return estudiantes
        except mysql.connector.Error as err:
            print(f"Error al listar estudiantes: {err}")

    def crear_estudiante(self, nombre, apellido, edad, sexo, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9):
        try:
            # Verificar si el estudiante ya existe
            self.cursor.execute(f"SELECT * FROM Estudiantes WHERE nombre = '{nombre}' AND apellido = '{apellido}'")
            estudiante_existente = self.cursor.fetchone()
            if estudiante_existente:
                print("El estudiante ya existe.")
                return False

            curso_asignado = self.asignar_curso(edad)
            if curso_asignado == 0:
                print("La edad del estudiante no corresponde a ningún curso conocido.")
                return False

            estudiante = {
                'atributo_1': atributo_1,
                'atributo_2': atributo_2,
                'atributo_3': atributo_3,
                'atributo_4': atributo_4,
                'atributo_5': atributo_5,
                'atributo_6': atributo_6,
                'atributo_7': atributo_7,
                'atributo_8': atributo_8,
                'atributo_9': atributo_9
            }

            # Obtener las casas de la base de datos
            
            casas = [
                hogwarts.consultar_casa(1),
                hogwarts.consultar_casa(2),
                hogwarts.consultar_casa(3),
                hogwarts.consultar_casa(4)
            ]

            casa_asignada = self.asignar_casa(estudiante, casas)
            if casa_asignada:
                codigo_casa_asignada = casa_asignada['codigo']
            else:
                codigo_casa_asignada = 0

            sql = f"INSERT INTO Estudiantes \
                   (nombre, apellido, edad, sexo, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9, casa_asignada, curso_asignado) \
                   VALUES \
                   ('{nombre}', '{apellido}', {edad}, '{sexo}', '{atributo_1}', '{atributo_2}', '{atributo_3}', '{atributo_4}', '{atributo_5}', '{atributo_6}', '{atributo_7}', '{atributo_8}', '{atributo_9}', {codigo_casa_asignada}, {curso_asignado})"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("Error al agregar estudiante:")
            print(f"Error code: {err.errno}")
            print(f"SQL State: {err.sqlstate}")
            print(f"Mensaje: {err.msg}")
            return False

    def asignar_casa(self, estudiante, casas):
        if estudiante is None:
            return None

        mejor_casa = None
        menor_distancia = float('inf')

        for casa in casas:
            distancia = self.calcular_distancia_atributos(estudiante, casa)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_casa = casa

        return mejor_casa

    def buscar_estudiante(self, nombre, apellido):
        try:
            self.cursor.execute(f"SELECT * FROM Estudiantes WHERE nombre = '{nombre}' AND apellido = '{apellido}'")
            estudiante = self.cursor.fetchone()
            return estudiante if estudiante else None
        except mysql.connector.Error as err:
            print(f"Error al buscar estudiante: {err}")
            return None    

    def calcular_distancia_atributos(self, estudiante, casa):
        suma_cuadrados = 0.0

        for atributo in estudiante:
            if atributo.startswith('atributo'):
                diferencia = estudiante[atributo] != casa[atributo]
                suma_cuadrados += diferencia ** 2

        distancia = math.sqrt(suma_cuadrados)
        return distancia

    def asignar_curso(self, edad):
        if 10 <= edad <= 14:
            return 1
        elif 15 <= edad <= 17:
            return 2
        elif 18 <= edad <= 20:
            return 3
        elif 21 <= edad <= 23:
            return 4
        elif 24 <= edad <= 25:
            return 5
        elif 26 <= edad <= 29:
            return 6
        else:
            return 7  # Para estudiantes mayores de 29 años
    
    # Consultar casa
    def obtener_estudiante(self, codigo):
        try:
            self.cursor.execute(f"SELECT * FROM Estudiantes WHERE codigo_identificacion = {codigo}")
            estudiante_exist = self.cursor.fetchone()
            if estudiante_exist:
                return estudiante_exist
        except mysql.connector.Error as err:
            print(f"Error al consultar estudiante: {err}")

    def actualizar_estudiante(self, codigo, nombre, apellido, edad, sexo, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9):
        try:
            sql = "UPDATE Estudiantes SET nombre=%s, apellido=%s, edad=%s, sexo=%s, atributo_1=%s, atributo_2=%s, atributo_3=%s, atributo_4=%s, atributo_5=%s, atributo_6=%s, atributo_7=%s, atributo_8=%s, atributo_9=%s WHERE codigo_identificacion=%s"
            data = (nombre, apellido, edad, sexo, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9, codigo)

            self.cursor.execute(sql, data)
            self.conn.commit()

            # Después de la actualización, obtener el estudiante actualizado
            estudiante_actualizado = self.obtener_estudiante(codigo)
            print(estudiante_actualizado)
            print(data)


            return estudiante_actualizado
        except mysql.connector.Error as err:
            print(f"Error al actualizar estudiante: {err}")
            return None
    





    def eliminar_estudiante(self, codigo):
        try:
            # Consultar el estudiante por código
            estudiante_exist = self.obtener_estudiante(codigo)

            if not estudiante_exist:
                print(f"No se encontró un estudiante con el código {codigo}")
                return False

            # Eliminar el estudiante de la base de datos
            sql = f"DELETE FROM Estudiantes WHERE codigo_identificacion = {codigo}"
            self.cursor.execute(sql)
            self.conn.commit()

            print(f"Estudiante con código {codigo} eliminado correctamente")
            return True

        except mysql.connector.Error as err:
            print(f"Error al eliminar estudiante: {err}")
            return False


def asignar_casa_por_atributos(self, atributos_actualizados, casas):
    if atributos_actualizados is None:
        return None

    mejor_casa = None
    menor_distancia = float('inf')

    for casa in casas:
        distancia = self.calcular_distancia_atributos(atributos_actualizados, casa)
        if distancia < menor_distancia:
            menor_distancia = distancia
            mejor_casa = casa

    return mejor_casa      
      

# Crear instancias de las clases
hogwarts = Casas(host='localhost', user='root', password='', database='datoshp')
estudiantes_hogwarts = Estudiantes(host='localhost', user='root', password='', database='datoshp')

# Agregar casas
hogwarts.crear_casa(1, 'Gryffindor', 'Valentia', 'Audacia', 'Lealtad', 'Cortecia', 'Amabilidad', 'Dignidad', 'Compañerismo', 'Fraternidad', 'Heroismo')
hogwarts.crear_casa(2, 'Slytherin', 'Ambicion', 'Astucia', 'Envidia', 'Perversión', 'Perspicacia', 'Ingenio', 'Astucia', 'Persuasión', 'Sagacidad')
hogwarts.crear_casa(3, 'Hufflepuff', 'Honor', 'Dedicación', 'Amistad', 'Justicia', 'Trabajo', 'Honestidad', 'Empatía', 'Paciencia', 'Benevolencia')
hogwarts.crear_casa(4, 'Ravenclaw', 'Inteligencia', 'Curiosidad', 'Creatividad', 'Sabiduria', 'Imaginación', 'Análisis', 'Sabiduría', 'Lógica', 'Erudición')

def obtener_atributos_casas():
    atributos = [
        {'nombre': 'Gryffindor', 'atributos': ['Valentia', 'Audacia', 'Lealtad', 'Cortesía', 'Amabilidad', 'Dignidad', 'Compañerismo', 'Fraternidad', 'Heroísmo']},
        {'nombre': 'Slytherin', 'atributos': ['Ambición', 'Astucia', 'Envidia', 'Perversión', 'Perspicacia', 'Ingenio', 'Astucia', 'Persuasión', 'Sagacidad']},
        {'nombre': 'Hufflepuff', 'atributos': ['Honor', 'Dedicación', 'Amistad', 'Justicia', 'Trabajo', 'Honestidad', 'Empatía', 'Paciencia', 'Benevolencia']},
        {'nombre': 'Ravenclaw', 'atributos': ['Inteligencia', 'Curiosidad', 'Creatividad', 'Sabiduría', 'Imaginación', 'Análisis', 'Sabiduría', 'Lógica', 'Erudición']}
    ]
    return atributos






# Crear estudiantes
estudiantes_hogwarts.crear_estudiante(
    'Harry', 'Potter', 10, 'M', 'Valentia', 'Astucia', 'Lealtad', 'Cortecia', 'Amabilidad', 'Dignidad', 'Valía', 'Paciencia', 'Erudición', 
)
estudiantes_hogwarts.crear_estudiante(
    'Hermione', 'Granger', 17, 'F', 'Valentia', 'Astucia', 'Lealtad', 'Cortecia', 'Amabilidad', 'Dignidad', 'Valía', 'Paciencia', 'Erudición',  
)
estudiantes_hogwarts.crear_estudiante(
    'Draco', 'Malfoy', 15, 'M', 'Ambición', 'Astucia', 'Envidia', 'Perversión', 'Perspicacia', 'Ingenio', 'Astucia', 'Persuasión', 'Sagacidad', 
)
estudiantes_hogwarts.crear_estudiante(
    'Ron', 'Weasley', 20, 'M', 'Valentia', 'Audacia', 'Lealtad', 'Cortesía', 'Trabajo', 'Honestidad', 'Empatía', 'Logica', 'Benevolencia', 
)


# Listar casas y estudiantes
hogwarts.listar_casas()
estudiantes_hogwarts.listar_estudiantes()


def obtener_estudiante(self, codigo):
    try:
        estudiante = self.obtener_estudiante(codigo)
        return jsonify(estudiante) if estudiante else jsonify({})
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({})



















@app.route('/', methods=['GET'])
def index():
    estudiantes = estudiantes_hogwarts.listar_estudiantes()
    return render_template('index4.html', datos_estudiantes=estudiantes, atributos=obtener_atributos_casas())

# @app.route('/editar_estudiante/<int:codigo>', methods=['GET'])
# def editar_estudiante(codigo):
#     # Obtener las opciones de atributos de las casas
#     atributos_casas = obtener_atributos_casas()
# 
#     # Obtener el estudiante a editar desde la base de datos
#     estudiante = estudiantes_hogwarts.obtener_estudiante(codigo)
# 
#     return render_template('index2.html', estudiante=estudiante, atributos=atributos_casas)

# Ruta para obtener los atributos de las casas
@app.route('/atributos_casas')
def atributos_casas():
    atributos = obtener_atributos_casas()
    return jsonify(atributos)





@app.route('/agregar_estudiante', methods=['POST'])
def agregar_estudiante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = int(request.form['edad'])
        sexo = request.form['sexo']
        atributo_1 = request.form['atributo_1']
        atributo_2 = request.form['atributo_2']
        atributo_3 = request.form['atributo_3']
        atributo_4 = request.form['atributo_4']
        atributo_5 = request.form['atributo_5']
        atributo_6 = request.form['atributo_6']
        atributo_7 = request.form['atributo_7']
        atributo_8 = request.form['atributo_8']
        atributo_9 = request.form['atributo_9']

        # Obtén los otros datos del formulario de manera similar

        exito = estudiantes_hogwarts.crear_estudiante(nombre, apellido, edad, sexo, atributo_1, atributo_2, atributo_3, atributo_4, atributo_5, atributo_6, atributo_7, atributo_8, atributo_9)  # Pasa todos los datos necesarios
        estudiantes_actualizados = estudiantes_hogwarts.listar_estudiantes()
        if exito:
            return redirect(url_for('index', mensaje='Estudiante agregado con éxito', tipo_mensaje='success'))
        else:
            return redirect(url_for('index', mensaje='Hubo un error al agregar al estudiante', tipo_mensaje='error'))

    return "Método no permitido"


@app.route('/consultar_estudiante', methods=['POST'])
def consultar_estudiante():
    if request.method == 'POST':
        nombre_consulta = request.json.get('nombre')
        apellido_consulta = request.json.get('apellido')
        
        # Buscar el estudiante por nombre y apellido en la base de datos
        estudiante = estudiantes_hogwarts.buscar_estudiante(nombre_consulta, apellido_consulta)
        
        if estudiante:
            return jsonify({'estudiante': estudiante})
        else:
            return jsonify({'estudiante': None})


@app.route('/obtener_estudiante/<int:codigo>', methods=['POST'])
def obtener_estudiante(codigo):
    try:
        # Verificar si todos los datos requeridos están presentes en la solicitud
        data = request.json
        required_fields = ['nombre', 'apellido', 'edad', 'sexo', 'atributo_1', 'atributo_2', 'atributo_3', 'atributo_4', 'atributo_5', 'atributo_6', 'atributo_7', 'atributo_8', 'atributo_9']

        if not all(field in data for field in required_fields):
            raise ValueError('Faltan datos requeridos en la solicitud')

        # Acceder a los datos usando get para proporcionar un valor predeterminado si la clave no está presente
        nombre = data.get('nombre', '')
        apellido = data.get('apellido', '')
        edad = data.get('edad', 0)
        sexo = data.get('sexo', '')
        atributo_1 = data.get('atributo_1', '')
        atributo_2 = data.get('atributo_2', '')
        atributo_3 = data.get('atributo_3', '')
        atributo_4 = data.get('atributo_4', '')
        atributo_5 = data.get('atributo_5', '')
        atributo_6 = data.get('atributo_6', '')
        atributo_7 = data.get('atributo_7', '')
        atributo_8 = data.get('atributo_8', '')
        atributo_9 = data.get('atributo_9', '')

        # Actualizar el estudiante en la base de datos
        exito = estudiantes_hogwarts.actualizar_estudiante(
            codigo,
            nombre,
            apellido,
            edad,
            sexo,
            atributo_1,
            atributo_2,
            atributo_3,
            atributo_4,
            atributo_5,
            atributo_6,
            atributo_7,
            atributo_8,
            atributo_9
        )

        if exito:
            return jsonify({'actualizado': True})
        else:
            return jsonify({'actualizado': False, 'mensaje': 'Error al actualizar el estudiante'})

    except ValueError as ve:
        return jsonify({'actualizado': False, 'mensaje': str(ve)})

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'actualizado': False, 'mensaje': 'Error al procesar la solicitud'})

@app.route('/listar_estudiantes', methods=['GET'])
def listar_estudiantes():
    estudiantes = estudiantes_hogwarts.listar_estudiantes()
    return jsonify(estudiantes)


@app.route('/eliminar_estudiante/<int:codigo>', methods=['DELETE'])
def eliminar_estudiante(codigo):
    try:
        # Llamar a la función eliminar_estudiante de la instancia de tu clase Estudiantes
        exito = estudiantes_hogwarts.eliminar_estudiante(codigo)

        if exito:
            return jsonify({'eliminado': True})
        else:
            return jsonify({'eliminado': False, 'mensaje': f'Error al eliminar el estudiante con código {codigo}'})

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'eliminado': False, 'mensaje': 'Error al procesar la solicitud'})

if __name__ == '__main__':
    app.run(debug=True, port=5006)

    