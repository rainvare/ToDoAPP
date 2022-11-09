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
