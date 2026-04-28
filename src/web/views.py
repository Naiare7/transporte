from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.services.actores_service import ActoresService
from src.services.logistica_service import LogisticaService
from src.services.transaccion_service import TransaccionService

web_bp = Blueprint("web", __name__, template_folder="../templates", static_folder="../static")

# Página de inicio
@web_bp.route("/")
def index():
    return render_template("index.html")

# ==================== CLIENTES ====================
@web_bp.route("/clientes")
def clientes_list():
    clientes = ActoresService.get_all_clientes()
    return render_template("clientes/list.html", clientes=clientes)

@web_bp.route("/clientes/new", methods=["GET", "POST"])
def clientes_new():
    if request.method == "POST":
        data = {
            "razon_social": request.form.get("razon_social"),
            "cif_nif": request.form.get("cif_nif"),
            "telefono": request.form.get("telefono"),
            "direccion": request.form.get("direccion")
        }
        ActoresService.create_cliente(data)
        flash("Cliente creado exitosamente", "success")
        return redirect(url_for("web.clientes_list"))
    return render_template("clientes/form.html", cliente=None)

@web_bp.route("/clientes/<int:id>/edit", methods=["GET", "POST"])
def clientes_edit(id):
    cliente = ActoresService.get_cliente_by_id(id)
    if request.method == "POST":
        data = {
            "razon_social": request.form.get("razon_social"),
            "cif_nif": request.form.get("cif_nif"),
            "telefono": request.form.get("telefono"),
            "direccion": request.form.get("direccion")
        }
        ActoresService.update_cliente(cliente, data)
        flash("Cliente actualizado exitosamente", "success")
        return redirect(url_for("web.clientes_list"))
    return render_template("clientes/form.html", cliente=cliente)

@web_bp.route("/clientes/<int:id>/delete", methods=["POST"])
def clientes_delete(id):
    cliente = ActoresService.get_cliente_by_id(id)
    ActoresService.delete_cliente(cliente)
    flash("Cliente eliminado exitosamente", "success")
    return redirect(url_for("web.clientes_list"))

# ==================== VEHÍCULOS ====================
@web_bp.route("/vehiculos")
def vehiculos_list():
    vehiculos = LogisticaService.get_all_vehiculos()
    return render_template("vehiculos/list.html", vehiculos=vehiculos)

@web_bp.route("/vehiculos/new", methods=["GET", "POST"])
def vehiculos_new():
    if request.method == "POST":
        data = {
            "patente": request.form.get("patente"),
            "capacidad_toneladas": float(request.form.get("capacidad_toneladas", 0)),
            "tipo_grano": request.form.get("tipo_grano"),
            "disponible": request.form.get("disponible") == "on"
        }
        LogisticaService.create_vehiculo(data)
        flash("Vehículo creado exitosamente", "success")
        return redirect(url_for("web.vehiculos_list"))
    return render_template("vehiculos/form.html", vehiculo=None)

@web_bp.route("/vehiculos/<int:id>/edit", methods=["GET", "POST"])
def vehiculos_edit(id):
    vehiculo = LogisticaService.get_vehiculo_by_id(id)
    if request.method == "POST":
        data = {
            "patente": request.form.get("patente"),
            "capacidad_toneladas": float(request.form.get("capacidad_toneladas", 0)),
            "tipo_grano": request.form.get("tipo_grano"),
            "disponible": request.form.get("disponible") == "on"
        }
        LogisticaService.update_vehiculo(vehiculo, data)
        flash("Vehículo actualizado exitosamente", "success")
        return redirect(url_for("web.vehiculos_list"))
    return render_template("vehiculos/form.html", vehiculo=vehiculo)

@web_bp.route("/vehiculos/<int:id>/delete", methods=["POST"])
def vehiculos_delete(id):
    vehiculo = LogisticaService.get_vehiculo_by_id(id)
    LogisticaService.delete_vehiculo(vehiculo)
    flash("Vehículo eliminado exitosamente", "success")
    return redirect(url_for("web.vehiculos_list"))

# ==================== PEDIDOS ====================
@web_bp.route("/pedidos")
def pedidos_list():
    pedidos = TransaccionService.get_all_pedidos()
    return render_template("pedidos/list.html", pedidos=pedidos)

@web_bp.route("/pedidos/new", methods=["GET", "POST"])
def pedidos_new():
    clientes = ActoresService.get_all_clientes()
    if request.method == "POST":
        data = {
            "cliente_id": int(request.form.get("cliente_id")),
            "usuario_id": 1,  # Temporal - idealmente del usuario logueado
            "estado": request.form.get("estado", "Pendiente"),
            "observaciones_entrega": request.form.get("observaciones_entrega")
        }
        TransaccionService.create_pedido(data)
        flash("Pedido creado exitosamente", "success")
        return redirect(url_for("web.pedidos_list"))
    return render_template("pedidos/form.html", pedido=None, clientes=clientes)

@web_bp.route("/pedidos/<int:id>/edit", methods=["GET", "POST"])
def pedidos_edit(id):
    pedido = TransaccionService.get_pedido_by_id(id)
    clientes = ActoresService.get_all_clientes()
    if request.method == "POST":
        data = {
            "cliente_id": int(request.form.get("cliente_id")),
            "estado": request.form.get("estado"),
            "observaciones_entrega": request.form.get("observaciones_entrega")
        }
        TransaccionService.update_pedido(pedido, data)
        flash("Pedido actualizado exitosamente", "success")
        return redirect(url_for("web.pedidos_list"))
    return render_template("pedidos/form.html", pedido=pedido, clientes=clientes)

@web_bp.route("/pedidos/<int:id>/delete", methods=["POST"])
def pedidos_delete(id):
    pedido = TransaccionService.get_pedido_by_id(id)
    TransaccionService.delete_pedido(pedido)
    flash("Pedido eliminado exitosamente", "success")
    return redirect(url_for("web.pedidos_list"))
