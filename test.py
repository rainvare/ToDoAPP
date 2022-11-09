from django.test import TestCase, override_settings
from todoapp.models import Task

#Pruebas para la clase Task del Model
class TaskTest(TestCase):
    def setUp(self):
        with override_settings(USE_TZ = True):
            Task.objects.create(title='Realizar test',description="Esta es una tarea de prueba", complete=False, date='2022-11-07' )

    def test_title(self):
        tarea = Task.objects.get(id=1)
        title = tarea._meta.get_field('title').verbose_name
        self.assertEqual (title, 'title')
    
    
    def test_date(self):
        tarea = Task.objects.get(id=1)
        date = tarea._meta.get_field('date').verbose_name
        self.assertEqual (date, 'date')
    
    def test_completion(self):
        tarea = Task.objects.get(id=1)
        complete = tarea._meta.get_field('complete').verbose_name
        self.assertEqual (complete, 'complete')
