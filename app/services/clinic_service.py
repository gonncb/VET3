from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.models.mascota import Mascota

class ClinicService:
    def __init__(self, cliente_repo: ClienteRepository):
        self.repo = cliente_repo

    def registrar_cliente_completo(self, dni, nombre, telefono, nombre_mascota, especie):
        if self.repo.buscar_por_dni(dni):
            return False 
        
        nuevo_cliente = Cliente(dni=dni, nombre=nombre, telefono=telefono)
        nueva_mascota = Mascota(nombre=nombre_mascota, especie=especie)
        nuevo_cliente.mascotas.append(nueva_mascota)
        
        self.repo.guardar(nuevo_cliente)
        return True
    
    def obtener_todos_clientes(self):
        return self.repo.buscar_todos()

    # --- ACTUALIZAR Y BORRAR DATOS ---
    def eliminar_cliente(self, id_cliente):
        cliente = self.repo.buscar_por_id(id_cliente)
        if cliente:
            self.repo.eliminar(cliente)
            return True
        return False

    def actualizar_cliente(self, id_cliente, nuevo_nombre, nuevo_telefono):
        cliente = self.repo.buscar_por_id(id_cliente)
        if cliente:
            cliente.nombre = nuevo_nombre
            cliente.telefono = nuevo_telefono
            self.repo.actualizar() # Hace commit de los cambios
            return True
        return False