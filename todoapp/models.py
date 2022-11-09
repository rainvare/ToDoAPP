from django.db import models
from django.contrib.auth.models import User

# Modelo de tarea mapeada con user de auth
class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null= True, blank= True
        )
    title = models.CharField(max_length = 150)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)


# Modelo self
def __str__(self):
    return self.title

#retorno valores de task realizadas
class Done:
    ordering = ['complete']