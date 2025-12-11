from datetime import date
from app.repositories.historial_repository import HistorialRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository # Nuevo import
from app.models.historial import HistorialMedico

class MedicalService:
    # Inyectamos también el repo de productos para poder restar stock
    def __init__(self, historial_repo: HistorialRepository, cliente_repo: ClienteRepository, producto_repo: ProductoRepository):
        self.historial_repo = historial_repo
        self.cliente_repo = cliente_repo
        self.producto_repo = producto_repo

    def buscar_cliente_por_dni(self, dni):
        return self.cliente_repo.buscar_por_dni(dni)

    def obtener_historial_mascota(self, id_mascota):
        return self.historial_repo.buscar_por_mascota(id_mascota)

    # --- MÉTODO ACTUALIZADO: AHORA GESTIONA PRODUCTOS ---
    def registrar_consulta(self, id_mascota, id_veterinario, diagnostico, descripcion, lista_ids_productos=None):
        """
        Registra la consulta y descuenta del stock los productos utilizados.
        """
        # 1. Crear la consulta básica
        nueva_consulta = HistorialMedico(
            fecha=date.today(),
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
            diagnostico=diagnostico,
            descripcion=descripcion
        )
        
        # 2. Gestionar Productos (Si se han seleccionado)
        if lista_ids_productos:
            for prod_id in lista_ids_productos:
                # Buscamos el producto
                producto = self.producto_repo.buscar_por_id(prod_id)
                if producto:
                    # A. Restamos Stock (1 unidad por uso en este ejemplo simple)
                    if producto.stock > 0:
                        producto.stock -= 1
                    
                    # B. Lo añadimos a la lista de "productos_utilizados" del historial
                    # SQLAlchemy gestionará la tabla intermedia automáticamente
                    nueva_consulta.productos_utilizados.append(producto)
        
        # 3. Guardar todo (Consulta + Relaciones + Cambios de Stock) de una vez
        return self.historial_repo.guardar(nueva_consulta)

    def eliminar_consulta(self, id_historial):
        consulta = self.historial_repo.buscar_por_id(id_historial)
        if consulta:
            self.historial_repo.eliminar(consulta)
            return True
        return False

    def actualizar_consulta(self, id_historial, nuevo_diagnostico, nueva_descripcion):
        consulta = self.historial_repo.buscar_por_id(id_historial)
        if consulta:
            consulta.diagnostico = nuevo_diagnostico
            consulta.descripcion = nueva_descripcion
            self.historial_repo.actualizar()
            return True
        return False