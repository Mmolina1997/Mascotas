from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId  # Importa ObjectId desde bson

app = Flask("Mi mascota")

# Configura la conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mascotas"]
collection = db["informacion"]

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/add_pet')
def addPet():
    return render_template('add_pet.html')

@app.route('/pets')
def index():
    mascotas = collection.find()
    return render_template('index.html', mascotas=mascotas)

@app.route('/agregar_mascota', methods=['POST'])
def agregar_mascota():
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    descripcion = request.form.get('descripcion')
   
    mascota = {
        "nombre": nombre,
        "tipo": tipo,
        "descripcion": descripcion,
        "adoptado": 0
    }

    collection.insert_one(mascota)
    return redirect(url_for('index'))

# Ruta para la página de edición de mascotas
@app.route('/editar_mascota/<mascota_id>')
def editar_mascota(mascota_id):
    mascota = collection.find_one({"_id": ObjectId(mascota_id)})
    if mascota:
        return render_template('editar.html', mascota=mascota)
    else:
        # Manejar el caso en el que la mascota no existe
        return "Mascota no encontrada", 404

# Ruta para guardar la edición de mascotas
@app.route('/guardar_edicion/<mascota_id>', methods=['POST'])
def guardar_edicion(mascota_id):
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    descripcion = request.form.get('descripcion')
    adoptado = request.form.get('adoptado')

    collection.update_one(
        {"_id": ObjectId(mascota_id)},
        {"$set": {"nombre": nombre, "tipo": tipo, "descripcion": descripcion, "adoptado": adoptado}}
    )

    return redirect(url_for('index'))

# Ruta para eliminar una mascota
@app.route('/eliminar_mascota/<mascota_id>', methods=['POST'])
def eliminar_mascota(mascota_id):
    collection.delete_one({"_id": ObjectId(mascota_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)