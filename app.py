from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)


flights = [
    {"id": 1, "name": "Vuelo A", "type": "Nacional", "price": 150.00},
    {"id": 2, "name": "Vuelo B", "type": "Internacional", "price": 300.00}
]
next_id = 3  

@app.route('/')
def home():
    return '''
    <h1>Bienvenido a la aplicaciónde gestión de vuelos y cálculo de factoriales</h1>
    <p>Seleccione una opción:</p>
    <a href="/flights"><button>Ver todos los vuelos</button></a>
    <a href="/add-flight-form"><button>Agregar un nuevo vuelo</button></a>
    <h2>Calcular Factorial</h2>
    <form action="/factorial" method="post">
        Número: <input type="number" name="number" min="0" required>
        <input type="submit" value="Calcular">
    </form>
    '''

@app.route('/factorial', methods=['POST'])
def factorial():
    try:
        number = int(request.form.get("number"))
        result = 1
        for i in range(1, number + 1):
            result *= i
        return f'''
        <h1>El factorial de {number} es {result}</h1>
        <a href="/"><button>Regresar al inicio</button></a>
        '''
    except ValueError:
        return '''
        <h1>Error: Entrada inválida</h1>
        <a href="/"><button>Regresar al inicio</button></a>
        '''

@app.route('/flights', methods=['GET'])
def get_flights():
    flights_list = ''.join([f"<li>{flight['name']} - {flight['type']} - ${flight['price']}</li>" for flight in flights])
    return f'''
    <h1>Lista de Vuelos</h1>
    <ul>{flights_list}</ul>
    <a href="/"><button>Regresar al inicio</button></a>
    '''

@app.route('/add-flight-form')
def add_flight_form():
    return '''
    <h1>Agregar un nuevo vuelo</h1>
    <form action="/flights" method="post">
        Nombre: <input type="text" name="name"><br>
        Tipo: 
        <select name="type">
            <option value="Nacional">Nacional</option>
            <option value="Internacional">Internacional</option>
        </select><br>
        Precio: <input type="number" step="0.01" name="price"><br>
        <input type="submit" value="Agregar vuelo">
    </form>
    <a href="/"><button>Regresar al inicio</button></a>
    '''

@app.route('/flights', methods=['POST'])
def add_flight():
    global next_id
    name = request.form.get("name")
    flight_type = request.form.get("type")
    price = request.form.get("price")
    
    if not name or not flight_type or not price:
        return '''
        <h1>Error: Información inválida</h1>
        <a href="/add-flight-form"><button>Intentar de nuevo</button></a>
        <a href="/"><button>Regresar al inicio</button></a>
        '''
    
    new_flight = {
        "id": next_id,
        "name": name,
        "type": flight_type,
        "price": float(price)
    }
    flights.append(new_flight)
    next_id += 1
    return f'''
    <h1>Vuelo agregado exitosamente</h1>
    <p>{new_flight['name']} - {new_flight['type']} - ${new_flight['price']}</p>
    <a href="/flights"><button>Ver todos los vuelos</button></a>
    <a href="/"><button>Regresar al inicio</button></a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
