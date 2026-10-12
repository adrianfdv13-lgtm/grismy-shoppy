from flask import Flask, render_template, request, redirect, url_for, session, flash
from collections import Counter

app = Flask(__name__)
app.secret_key = "grismy-shoppy-demo-local"

PRODUCTOS = [
    {"id": 1, "nombre": "Laptop 15.6 pulgadas", "categoria": "Computadoras", "precio": 499.99, "emoji": "💻", "descripcion": "Para estudiar, trabajar y usar tus aplicaciones."},
    {"id": 2, "nombre": "Audífonos Bluetooth", "categoria": "Electrónicos", "precio": 39.99, "emoji": "🎧", "descripcion": "Sonido inalámbrico para música y llamadas."},
    {"id": 3, "nombre": "Mouse inalámbrico", "categoria": "Computadoras", "precio": 19.99, "emoji": "🖱️", "descripcion": "Práctico para estudiar y trabajar."},
    {"id": 4, "nombre": "Teclado mecánico RGB", "categoria": "Computadoras", "precio": 49.99, "emoji": "⌨️", "descripcion": "Teclado iluminado para estudiar y jugar."},
    {"id": 5, "nombre": "Monitor Full HD", "categoria": "Computadoras", "precio": 179.99, "emoji": "🖥️", "descripcion": "Pantalla para tu escritorio."},
    {"id": 6, "nombre": "Teléfono inteligente", "categoria": "Celulares", "precio": 299.99, "emoji": "📱", "descripcion": "Un teléfono para aplicaciones y fotografías."},
    {"id": 7, "nombre": "Silla gamer", "categoria": "Hogar y oficina", "precio": 149.99, "emoji": "🪑", "descripcion": "Comodidad para tu espacio de estudio."},
    {"id": 8, "nombre": "Reloj inteligente", "categoria": "Electrónicos", "precio": 59.99, "emoji": "⌚", "descripcion": "Consulta notificaciones desde tu muñeca."},
    {"id": 9, "nombre": "Mochila urbana", "categoria": "Moda", "precio": 29.99, "emoji": "🎒", "descripcion": "Lleva tus materiales y accesorios."},
    {"id": 10, "nombre": "Consola de videojuegos", "categoria": "Videojuegos", "precio": 399.99, "emoji": "🎮", "descripcion": "Entretenimiento para tus ratos libres."},
    {"id": 11, "nombre": "Zapatillas deportivas", "categoria": "Moda", "precio": 64.99, "emoji": "👟", "descripcion": "Estilo casual para todos los días."},
    {"id": 12, "nombre": "Altavoz portátil", "categoria": "Electrónicos", "precio": 34.99, "emoji": "🔊", "descripcion": "Música en un formato compacto."},
]

@app.context_processor
def datos_globales():
    carrito = session.get("carrito", {})
    return {"cantidad_carrito": sum(int(v) for v in carrito.values())}

def carrito_detallado():
    carrito = session.get("carrito", {})
    items, total, cantidad = [], 0, 0
    for p in PRODUCTOS:
        n = int(carrito.get(str(p["id"]), 0))
        if n > 0:
            subtotal = p["precio"] * n
            items.append({"producto": p, "cantidad": n, "subtotal": subtotal})
            total += subtotal
            cantidad += n
    return items, total, cantidad

@app.route("/")
def inicio():
    q = request.args.get("q", "").strip()
    cat = request.args.get("categoria", "").strip()
    productos = PRODUCTOS
    if q:
        productos = [p for p in productos if q.casefold() in p["nombre"].casefold() or q.casefold() in p["categoria"].casefold()]
    if cat:
        productos = [p for p in productos if p["categoria"] == cat]
    categorias = sorted({p["categoria"] for p in PRODUCTOS})
    return render_template("index.html", productos=productos, categorias=categorias, busqueda=q, categoria=cat)

@app.route("/agregar/<int:pid>", methods=["POST"])
def agregar(pid):
    if any(p["id"] == pid for p in PRODUCTOS):
        carrito = session.get("carrito", {})
        clave = str(pid)
        carrito[clave] = int(carrito.get(clave, 0)) + 1
        session["carrito"] = carrito
        flash("¡Producto agregado al carrito!")
    return redirect(request.referrer or url_for("inicio"))

@app.route("/carrito")
def ver_carrito():
    items, total, cantidad = carrito_detallado()
    return render_template("carrito.html", items=items, total=total, cantidad=cantidad, categorias=sorted({p["categoria"] for p in PRODUCTOS}), busqueda="", categoria="")

@app.route("/quitar/<int:pid>", methods=["POST"])
def quitar(pid):
    carrito = session.get("carrito", {})
    carrito.pop(str(pid), None)
    session["carrito"] = carrito
    flash("Producto quitado.")
    return redirect(url_for("ver_carrito"))

@app.route("/vaciar", methods=["POST"])
def vaciar():
    session["carrito"] = {}
    flash("Carrito vaciado.")
    return redirect(url_for("ver_carrito"))

@app.route("/finalizar", methods=["POST"])
def finalizar():
    items, total, cantidad = carrito_detallado()
    if not items:
        flash("Tu carrito está vacío.")
        return redirect(url_for("ver_carrito"))
    session["carrito"] = {}
    return render_template("confirmacion.html", total=total, cantidad=cantidad, categorias=sorted({p["categoria"] for p in PRODUCTOS}), busqueda="", categoria="")

if __name__ == "__main__":
    # Acceso desde esta laptop y otros dispositivos de la misma red local:
    # Usa 127.0.0.1 para solo esta laptop; cambia a 0.0.0.0 para compartir por Wi-Fi.
    app.run(host="127.0.0.1", port=5000, debug=False)
