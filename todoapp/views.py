from django.shortcuts import render
#imports CRUD
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
#import response
from django.urls import reverse_lazy

#import users auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

#logs
import logging
mylogger= logging.getLogger('mylog')




#________________AUTH___________________
#Inicio de sesión
class UserLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        mylogger.debug('Petición exitosa de url')
        return reverse_lazy('lista-tareas')

#Registro de usuario
class UserRegisterView(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('lista-tareas')

    #Validación de registro y redirección de usuario
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            mylogger.debug('Intento de ingreso de user no registrado, redirección a login')
            login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)
    
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            mylogger.debug('Login y Usuario autenticado')
            #return redirect('tasks')
        return super(UserRegisterView, self).get(*args, **kwargs)


# _________ Views de clase _____________

#Lista de tareas
class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name ='tasks'

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

# Detalle de tarea
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name ='task'
    template_name = 'todoapp/task.html'

# Crear tareas
class TaskCreate(LoginRequiredMixin, CreateView):
    model= Task
    #fields = '__all__'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/form.html'

    # asociar un user a una tarea en el form
    def form_valid(self, form):
        mylogger.debug('Validado el user en el form de creación de tarea')
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#Editar tareas
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/form.html'

# Eliminar Tareas
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('lista-tareas')
    template_name = 'todoapp/delete.html'
  



