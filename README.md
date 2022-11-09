# Esta es mi TO DO APP :heart:

El propósito de este proyecto fue crear una pequeña app de tareas, la cual cumpla con los siguientes requerimientos:


## Requerimientos:

- Registro y Login de usuarios con autenticación
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

### Requerimientos opcionales:
- Logs
- Test
- Dockerización

## :star: ¿Qué herramientas utilicé? :star: :

- Python para codear
- Django como framework
- sqlite para mi base de datos
- Docker para ejecutar el proyecto en cualquier ambiente

## :star: ¿Cómo desarrollé el proyecto? :star: :

Primero, cree un entorno virtual para mi proyecto con [virtualenv](https://pypi.org/project/pipenv/).
Procedí a instalar los programas necesarios para construir mi app, como python y django con pip:

```cmd
pip install django
```
Luego cree mi proyecto con Django de la siguiente manera:

```cmd
django-admin startproject todoproject
```
Lo siguiente en la lista fue crear mi app:
```cmd
python manage.py startapp todoapp
```
Una vez creada mi app, fui a configurarla en mi proyecto, archivo *setting.py* :
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todoapp', #justo aquí
]
```
Como última forma de conectar mi project y mi app, enlacé los archivos URL para que pudieran relacionarse los path de mis vistas de app con el proyecto 

### El modelo
En mi todoapp realicé un model de clase llamado Task, el cual setee con el model User de Django. Este modelo contiene los atributos de título, descripción, fecha de creación (seteada de manera automática) y un valor booleano para definir si la tarea ha sido completada o no:
```python
class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null= True, blank= True
        )
    title = models.CharField(max_length = 150)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
```
Una vez creado el modelo de Tarea, lo registré en mi archivo *admin.py* de la app:
```python
from django.contrib import admin
from .models import Task

#registro mi app en el panel de admin
admin.site.register(Task)
```
Y realicé un migrate para llevar este modelo a la base de datos sqlite que provee django
```cmd
python manage.py migrate
```
-----------
### El CRUD
En el archivo *views.py* cree las vistas que se conectarían con mi template y me permitirían ver, listar, editar y borrar una tarea:
```python
#Lista de tareas
class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name ='tasks'

# Detalle de tarea
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name ='task'
    template_name = 'todoapp/task.html'    

# Crear tareas
class TaskCreate(LoginRequiredMixin, CreateView):
    model= Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/form.html'
    
#Editar tareas
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/form.html'
    
#Eliminar Tareas
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/delete.html'    
```
#### Los endpoints
Con el fin de crear las rutas o endpoints de mi API configuré los PATH en el archivo de mi app *urls.py* :
```python
from django.urls import path
from .views import UserRegisterView, UserLoginView, TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete
from django.contrib.auth.views import LogoutView

#Config de URLs de app

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login" ),
    path('register/', UserRegisterView.as_view(), name="register" ),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout" ),
    path('', TaskList.as_view(), name='lista-tareas'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='detalle-tarea-id'),
    path('create-task/', TaskCreate.as_view(), name='crear-tarea'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='editar-tarea-id'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='borrar-tarea'),
    
]
```
#### Los templates
Una vez estuvo desarrollada mi API, cree una carpeta Templates donde guardar mis archivos html que servirían de base para mi front:
Tanto para los formularios de Registro, Login y Creación de Tarea use una validación. 
```html
 <form method="POST">
    {% csrf_token %} {{form.as_p}}
    <input class="button" type="submit" value="Login" />
  </form>
```

### Filtros de usuario, título de tarea y fecha de creación de tarea

Además, cree un filtro con context para validar los datos que podían verser y los fitros de búsqueda de tareas
```python
#filtros de datos de usuario con context_data  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.model.objects.filter(user=self.request.user)
        context['count'] = self.model.objects.filter(complete=False).count()

        #filtro de búsqueda por tarea
        filterByTitle = self.request.GET.get('filterByTitle') or ''
        if filterByTitle:
            mylogger.debug('Se realiza filtrado por nombre de tarea')
            context['tasks'] = context['tasks'].filter(
                title__contains=filterByTitle)
        context['filterByTitle'] = filterByTitle

        #filtro de búsqueda por fecha
        filterByDate = self.request.GET.get('filterByDate') or ''
        if filterByDate:
            mylogger.debug('Se realiza filtrado por fecha de tarea')
            context['tasks'] = context['tasks'].filter(
                date__contains=filterByDate)
        context['filterByDate'] = filterByDate

        return context
```
Por último:
- Utilicé Logging para hacer log en modo debug y llevar un control del flujo de la app.
- TestCase para realizar unos testeos sencillos del modelo de tarea
- Y me animé a Crear un Dockerfile y un Dockercompose.yml para dockerizar todo el proyecto

## :star: Vamos a ver si anda... :star: :
Para iniciar este proyecto debe activar el ambiente virtual:
```cmd
source ./Scripts/activate
```
Instale también los programas necesarios para la app
```cmd
pip install -r .\requirement.txt
```
Y levantar el server de Django
```cmd
python manage.py runserver
```
Esto lo puede hacer con docker igualmente
```cmd
docker build -t (PATH)
```

## :star: Ahora quiero testearlo :star: :

### REST API UNIT TESTING

Esta es la parte divertida, puede crear tareas, eliminarlas o filtrarlas con el front y realizar un testeo manual.
Sin embargo, para su diversión, agregué tres pequeños test creados con TestCase de Django. De manera que pueda ver cómo funcionan este tipo de pruebas a detalle.
```cmd
python manage.py test
```
Con ello, correrá el archivo *test.py* de la carpeta raíz


## ¿Hemos terminado?

JA.. lo dudo. Si bien llegué a concluir un proyecto ajustado a los requerimientos en el proceso descubrí que, aún tengo algunas dificultades por eso sé que muchas cosas de mi código podrían mejorar. Sin embargo, la experiencia de contruir este proyecto ha sido muy divertida y probablemente vuelva a él en algún tiempo para realizar una versión 2.0.

Si tú, querido dev, has llegado hasta acá. Pues, te agradezco por leerme y acompañarme en el camino de construir este proyecto.
Uff, ahora sí ya terminamos... 


## Creado por una aprendiz de código:

* Author: [R. Indira Valentina Réquiz Molina](https://github.com/rainvare) 
* Email:  [indirarequiz@gmail.com]
* Cualquier mejora es bienvenida!!
* Happy Coding!!

### License

```
MIT License

Copyright (c) 2022 rainvare

```
