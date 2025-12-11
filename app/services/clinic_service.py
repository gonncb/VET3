from collections import Counter
from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.models.mascota import Mascota

class ClinicService:
    def __init__(self, cliente_repo: ClienteRepository):
        self.repo = cliente_repo

    def registrar_cliente_completo(self, dni, nombre, telefono, nombre_mascota, especie):
        """
        Registra un cliente nuevo y su primera mascota en una sola transacción.
        Devuelve True si tiene éxito, False si el DNI ya existe.
        """
        # 1. Validación de Negocio: ¿Existe el DNI?
        if self.repo.buscar_por_dni(dni):
            return False  # El cliente ya existe
        
        # 2. Crear Entidades
        nuevo_cliente = Cliente(dni=dni, nombre=nombre, telefono=telefono)
        # Creamos la mascota pero NO la guardamos todavía
        nueva_mascota = Mascota(nombre=nombre_mascota, especie=especie)
        
        # 3. Asociar (La magia de ORM)
        # Al añadir la mascota a la lista del cliente, SQLAlchemy entiende la relación
        nuevo_cliente.mascotas.append(nueva_mascota)
        
        # 4. Persistir (Guardar padre e hijo a la vez)
        self.repo.guardar(nuevo_cliente)
        return True
    
    def obtener_todos_clientes(self):
        """Devuelve la lista completa de clientes con sus mascotas"""
        return self.repo.buscar_todos()

    # --- FUNCIONALIDADES CRUD (Eliminar y Editar) ---
    
    def eliminar_cliente(self, id_cliente):
        """
        Elimina un cliente por su ID.
        Al tener 'cascade' configurado en el modelo, se borrarán sus mascotas automáticamente.
        """
        cliente = self.repo.buscar_por_id(id_cliente)
        if cliente:
            self.repo.eliminar(cliente)
            return True
        return False

    def actualizar_cliente(self, id_cliente, nuevo_nombre, nuevo_telefono):
        """Actualiza los datos básicos de un cliente"""
        cliente = self.repo.buscar_por_id(id_cliente)
        if cliente:
            cliente.nombre = nuevo_nombre
            cliente.telefono = nuevo_telefono
            self.repo.actualizar() # Confirma los cambios en la DB
            return True
        return False

    # --- FUNCIONALIDADES PARA DASHBOARD (Gráficos) ---

    def obtener_estadisticas_especies(self):
        """
        Cuenta cuántas mascotas hay de cada tipo para el gráfico circular.
        Devuelve un objeto Counter (ej: {'Perro': 5, 'Gato': 2})
        """
        clientes = self.repo.buscar_todos()
        especies = []
        
        # Recorremos todos los clientes y todas sus mascotas
        for c in clientes:
            for m in c.mascotas:
                especies.append(m.especie)
        
        return Counter(especies)