
from django.test import TestCase
from asesorias.models import Asesoria, Curso, Seccion, FactTable, Cita
from asesorias.views import grabar_Asesoria,grabar_fact,validarAsesoria
from accounts.models import User
from accounts.views import crearCita
from django.test.client import Client




class Views_test(TestCase):

    def setUp(self):
        print("se inicia el test")
        profesor=User.objects.create(is_admin=True,first_name="Pavel",last_name="Bardelli",email="a@gmail.com")
        curso=Curso.objects.create(nombre="TPI",creditos=2,nivel=6)
        seccion=Seccion.objects.create(codigo=801,curso=curso,profesor=profesor)
        Asesoria.objects.create(dia="lunes",horario="11-12",lugar="TA 802",seccion=seccion)

    def tearDown(self):
        print("Se termina el test")
    def test_grabar_Asesoria(self):
        print("test Aesoria")
        seccion=Seccion.objects.get(codigo=801)
        #self.assert(grabar_Asesoria("lunes","11-12","TA 802",seccion))
        self.assertIsInstance(grabar_Asesoria("lunes","11-12","TA 802",seccion),Asesoria)
    def test_grabar_fact(self):
        print("test FactTable")
        curso=Curso.objects.get(nombre="TPI")
        profesor=User.objects.get(first_name="Pavel")
        asesoria=Asesoria.objects.get(dia="lunes")
        seccion=Seccion.objects.get(codigo=801)
        #cambiar en grabar fact el return
        self.assertIsInstance(grabar_fact(curso,profesor,asesoria,seccion),FactTable)
    def test_validarAsesoria(self):

        seccion=Seccion.objects.get(codigo=801)
        dia="lunes"
        lugar="TA 802"
        horario="11-12"  
        self.assertTrue(validarAsesoria(dia,horario,lugar,seccion))
        self.assertFalse(validarAsesoria(dia,"10-11",lugar,seccion))
    def test_crearCita(self):
        #def crearCita(alumno,asesoria,comentario,estado,fechaCita):
        #    cita= Cita.objects.create(alumno_id= alumno, asesoria_id=asesoria,comentario=comentario, estado=estado,fechaCita=fechaCita)
        #    cita.save()
        #    return True
        print("test Crear Cita")
        self.assertTrue(crearCita(1,1,"Hola",True,"2018-01-11"))

    def test_validate_curso(self):
        c = Client()

        #response = c.get('/validate_curso')
        response = c.get('/validate_curso', {'curso': 'TPI'})
        self.assertEqual(response.status_code, 200)

    #def test_uploadFiles(self)
    #    h = uploadFiles()
    #    se
    #    self.assertEqual()

    #def test_form(self):
    #    asesoria = Asesoria(dia="Lunes", horario="Viernes", lugar="R205")
    #    self.assertEqual(str(asesoria), asesoria.dia, asesoria.horario)



#class CursoModelTest(TestCase):
#
#    def test_string_representation(self):
#        curso = Curso(nombre="ERP")
#        self.assertEqual(str(curso), curso.nombre)


#class SeccionTest(TestCase):
#
#    def test_seccion(self):

#        secc = Seccion(codigo=801)
#        self.assertEqual(str(secc),secc.codigo)

#class AsesoriaModelTest(TestCase):
#
#    def test_form(self):
#        asesoria = Asesoria(dia="Lunes", horario="Viernes", lugar="R205")
#
#        self.assertEqual(str(asesoria), asesoria.dia, asesoria.horario)







#class grabar_Asesoria_test(TestCase):
#
#    def test_form(self):
#        var1 = User.objects.create(first_name ="Irey", last_name ="Quintana", email ="123@gmail.com")
#        var2 = Curso.objects.create(nombre="Erp", creditos = 3 , nivel=8)
#        obj = Seccion.objects.create(codigo=12, curso=var2, profesor=var1)
#        grabar = grabar_Asesoria(dia="Lunes", horario="Viernes", lugar="R205",objSeccion=obj)
#        resp = grabar.save()
#        self.assertFalse(resp)
