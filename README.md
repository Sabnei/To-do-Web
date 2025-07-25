# 📋 Gestor de Tareas con Django y Bootstrap

Una aplicación web moderna y responsive para gestionar tareas personales y profesionales, desarrollada con Django y Bootstrap 5.

## ✨ Características

### 🎨 Diseño Moderno
- **Bootstrap 5**: Interfaz moderna y responsive
- **Font Awesome**: Iconos profesionales
- **Gradientes y efectos**: Diseño atractivo con efectos visuales
- **Animaciones CSS**: Transiciones suaves y efectos hover
- **Modo oscuro**: Soporte opcional para modo oscuro

### 📊 Dashboard Interactivo
- **Página de inicio**: Estadísticas en tiempo real
- **Cards informativas**: Resumen visual de tareas
- **Tareas urgentes**: Vista rápida de prioridades altas
- **Tareas recientes**: Últimas tareas creadas
- **Acciones rápidas**: Acceso directo a funciones principales

### 🔍 Filtros Avanzados
- **Por prioridad**: Alta, Media, Baja
- **Por estado**: Completadas, Pendientes
- **Por etiquetas**: Búsqueda por palabras clave
- **Filtros combinados**: Múltiples criterios simultáneos

### 📝 Gestión de Tareas
- **Crear tareas**: Formulario intuitivo con validación
- **Editar estado**: Marcar como completada/pendiente
- **Eliminar tareas**: Con confirmación de seguridad
- **Prioridades**: Sistema de prioridades visual
- **Fechas límite**: Control de deadlines
- **Etiquetas**: Organización por categorías

### 📄 Exportación
- **Exportar a PDF**: Generación de reportes
- **Filtros aplicados**: Respeta los filtros activos
- **Formato profesional**: Diseño limpio para impresión

## 🚀 Tecnologías Utilizadas

- **Backend**: Django 4.x
- **Frontend**: Bootstrap 5.3.0
- **Iconos**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JS con efectos modernos
- **CSS**: Estilos personalizados con variables CSS
- **Base de datos**: SQLite (configurable)

## 📦 Instalación

1. **Clonar el repositorio**:
```bash
git clone <url-del-repositorio>
cd To-do-Web
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**:
```bash
cd todo_web
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario** (opcional):
```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor**:
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**:
```
http://localhost:8000
```

## 🎯 Funcionalidades Principales

### Página de Inicio (`/`)
- Dashboard con estadísticas en tiempo real
- Vista de tareas urgentes
- Tareas recientes
- Acciones rápidas

### Lista de Tareas (`/tareas/`)
- Vista en cards responsive
- Filtros avanzados
- Exportación a PDF
- Acciones por tarea

### Nueva Tarea (`/agregar/`)
- Formulario con validación en tiempo real
- Contador de caracteres
- Sugerencias de etiquetas
- Diseño moderno

## 🎨 Características de Diseño

### Responsive Design
- **Mobile First**: Optimizado para dispositivos móviles
- **Grid System**: Layout adaptativo de Bootstrap
- **Breakpoints**: Adaptación automática a diferentes pantallas

### Efectos Visuales
- **Hover Effects**: Animaciones en cards y botones
- **Transiciones**: Movimientos suaves entre estados
- **Gradientes**: Fondos modernos con gradientes CSS
- **Sombras**: Efectos de profundidad

### Interactividad
- **JavaScript**: Validación en tiempo real
- **Confirmaciones**: Diálogos de confirmación
- **Animaciones**: Efectos de carga y transición
- **Tooltips**: Información contextual

## 📱 Compatibilidad

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🔧 Configuración Avanzada

### Variables CSS Personalizadas
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}
```

### Personalización de Colores
Los colores y gradientes se pueden personalizar modificando las variables CSS en `static/tareas/css/style.css`.

## 📊 Estructura del Proyecto

```
todo_web/
├── tareas/
│   ├── templates/tareas/
│   │   ├── base.html          # Template base con Bootstrap
│   │   ├── inicio.html        # Dashboard principal
│   │   ├── lista_tareas.html  # Lista con filtros
│   │   └── agregar_tarea.html # Formulario de creación
│   ├── static/tareas/
│   │   ├── css/style.css      # Estilos personalizados
│   │   └── js/app.js          # JavaScript interactivo
│   ├── models.py              # Modelo de datos
│   ├── views.py               # Lógica de negocio
│   ├── forms.py               # Formularios
│   └── urls.py                # Rutas de la aplicación
└── todo_web/
    ├── settings.py            # Configuración de Django
    └── urls.py                # URLs principales
```

## 🚀 Despliegue

### Heroku
1. Crear `Procfile`:
```
web: gunicorn todo_web.wsgi --log-file -
```

2. Configurar variables de entorno:
```bash
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DEBUG=False
```

3. Desplegar:
```bash
git push heroku main
```

### Docker
1. Crear `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Bootstrap Team**: Por el increíble framework CSS
- **Font Awesome**: Por los iconos profesionales
- **Django Community**: Por el framework web robusto

---

**Desarrollado con ❤️ usando Django y Bootstrap**