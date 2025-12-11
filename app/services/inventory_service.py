from app.repositories.producto_repository import ProductoRepository
from app.models.producto import Producto

class InventoryService:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def obtener_todos(self):
        return self.repo.buscar_todos()

    def crear_producto(self, nombre, categoria, precio, stock_inicial):
        nuevo_prod = Producto(
            nombre=nombre, 
            categoria=categoria, 
            precio=float(precio), 
            stock=int(stock_inicial)
        )
        return self.repo.guardar(nuevo_prod)

    def actualizar_stock(self, id_producto, cantidad, operacion="sumar"):
        prod = self.repo.buscar_por_id(id_producto)
        if prod:
            if operacion == "sumar":
                prod.stock += int(cantidad)
            elif operacion == "restar":
                # Evitar stock negativo (validación simple)
                prod.stock = max(0, prod.stock - int(cantidad))
            
            self.repo.actualizar_stock()
            return True
        return False

    def eliminar_producto(self, id_producto):
        prod = self.repo.buscar_por_id(id_producto)
        if prod:
            self.repo.eliminar(prod)
            return True
        return False
        
    def obtener_producto_por_id(self, id):
        return self.repo.buscar_por_id(id)