
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from .models import User
from asesorias.models import Asesoria, Curso, Seccion, FactTable, Cita
from django.http import JsonResponse
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def mostrarCursos(request):
    agregar = 1
    tipo = 0
    curso = Curso.objects.all().order_by('id')

    return render(request, 'agregarAsesoria.html', locals())



def listarAsesoria(request):
    tipo = 0
    agregar = 0
    factTable = FactTable.objects.all().order_by("id")
    arreglo=[]

    for x in factTable:

        x_info = {}

        #CURSO
        curso= Curso.objects.filter(id=x.curso_id)
        for y in curso:
            x_info['curso'] = y.nombre

        #PROFESOR
        profesor=User.objects.filter(id=x.profesor_id)
        for y in profesor:
            x_info['profesor'] = y.first_name
            x_info['profesor2'] = y.last_name

        #ASESORIA
        asesoria=Asesoria.objects.filter(id=x.asesoria_id)
        for y in asesoria:
            x_info['id'] = y.id
            x_info['horario'] = y.horario
            x_info['dia'] = y.dia
            x_info['lugar'] = y.lugar

        #Seccion
        seccion=Seccion.objects.filter(id=x.seccion_id)
        for y in seccion:
            x_info['seccion'] = y.codigo

        arreglo.append(x_info)
    print(arreglo)

    return render(request, 'listarAsesoria.html', locals())

def eliminarAsesoria(request):
    tipo = 0
    agregar = 0
    id=request.POST.get('id_asesoria', False)
    asesoria=Asesoria.objects.filter(id=id)
    FactTable.objects.filter(asesoria=asesoria)
    asesoria.delete()
    return redirect('/listarAsesoria')

def editarAsesoria(request):

    #id de asesoria
    id = int(request.GET.get('id'))
    curso = str(request.GET.get('curso'))
    dia = str(request.GET.get('dia'))
    lugar = str(request.GET.get('lugar'))
    profesor = str(request.GET.get('profesor'))
    seccion = str(request.GET.get('seccion'))
    horario = str(request.GET.get('horario'))
    cursos = Curso.objects.all().order_by('id')
    tipo= 1
    agregar= 0
    asesoria= Asesoria.objects.get(id=id)
    objProf= User.objects.get(first_name=profesor)
    profesor2=objProf.last_name
    objCurso= Curso.objects.get(nombre=curso)
    objSeccion=Seccion.objects.get(profesor=objProf.id,curso=objCurso.id,codigo=int(seccion))
    fact=FactTable.objects.get(curso=objCurso,profesor=objProf,asesoria=asesoria,seccion=objSeccion)
    fact_id=fact.id
    listado = Asesoria.objects.all().order_by("id")

    return render(request, 'editarAsesoria.html', locals())


def actualizarAsesoria(request):
    tipo = 0
    agregar = 0
    id=request.POST.get('id_asesoria', False)
    fact_id=int(request.POST.get('id_fact', False))
    curso=request.POST['curso']
    profesor=request.POST['profesor']
    horario=request.POST['horario']
    seccion=request.POST['seccion']
    lugar=request.POST['lugar']
    dia=request.POST['dias']
    arrProf=profesor.split(" ")
    if len(arrProf) > 1:
        objProf= User.objects.get(first_name=arrProf[0])
    else:
        objProf= User.objects.get(first_name=profesor)
    objCurso= Curso.objects.get(nombre=curso)
    objSeccion=Seccion.objects.get(profesor=objProf.id,curso=objCurso.id,codigo=int(seccion))
    if validarAsesoria(dia,horario,lugar,objSeccion) :

        errorRep=0
        cursos = Curso.objects.all().order_by('id')
        return render(request, 'editarAsesoria.html',locals())
    else:
        asesoria= Asesoria.objects.get(id=id)
        asesoria.curso = curso
        asesoria.profesor = profesor
        asesoria.horario = horario
        asesoria.lugar = lugar
        asesoria.dia=dia
        asesoria.save()
        print(fact_id)

        fact=FactTable.objects.get(id=fact_id)
        fact.profesor=objProf
        fact.curso=objCurso
        fact.seccion=objSeccion
        fact.save()

        #return render(request, 'listarAsesoria.html', locals())
        return redirect('/listarAsesoria')

def validarAsesoria(dia,horario,lugar,seccion):
    buscarAsesoria=Asesoria.objects.filter(dia__iexact=dia,horario__iexact=horario,lugar__iexact=lugar)
    buscarAsesoriaSeccion=Asesoria.objects.filter(dia__iexact=dia,horario__iexact=horario,seccion=seccion)
    if buscarAsesoria or buscarAsesoriaSeccion:
        return True
    else:
        return False
def grabar_Asesoria(dia,horario,lugar,objSeccion):
    asesoria = Asesoria.objects.create(dia=dia, horario=horario, lugar=lugar, seccion=objSeccion)
    asesoria.save()
    return asesoria
def grabar_fact(objCurso,objProf,newAsesoria,objSeccion):
    fact=FactTable.objects.create(curso=objCurso,profesor=objProf,asesoria=newAsesoria,seccion=objSeccion)
    fact.save()
    return fact

def guardarAsesoria(request):
    errorRep=1
    tipo = 0
    agregar = 0
    curso=request.POST['curso']
    sv=request.POST['seccion']
    profesor=request.POST['profesor']
    horario=request.POST['horario']
    seccion=request.POST['seccion']
    dia=request.POST['dia']
    print(profesor)
    lugar=request.POST['lugar']
    objCurso= Curso.objects.get(nombre=curso)
    arrProf=profesor.split(" ")
    objProf= User.objects.get(first_name=arrProf[0])
    objProf2= User.objects.get(last_name=arrProf[1])
    print(arrProf[0])
    if objProf.id==objProf2.id:
        objSeccion=Seccion.objects.get(profesor=objProf.id,curso=objCurso.id,codigo=int(seccion))
    if validarAsesoria(dia,horario,lugar,objSeccion) :
        print("REPETIDOOOO")
        errorRep=0
        curso = Curso.objects.all().order_by('id')
        #return redirect('/agregarAsesoria',locals())
        return render(request, 'agregarAsesoria.html',locals())
    else:
        #asesoria = Asesoria.objects.create(dia=dia, horario=horario, lugar=lugar, seccion=objSeccion)
        #asesoria.save()
        newAsesoria=grabar_Asesoria(dia,horario,lugar,objSeccion)
        print(newAsesoria)
        #fact=FactTable.objects.create(curso=objCurso,profesor=objProf,asesoria=newAsesoria,seccion=objSeccion)
        #fact.save()
        grabar_fact(objCurso,objProf,newAsesoria,objSeccion)
        return redirect('/listarAsesoria')
    return 0
def cancelar(request):
    tipo = 0
    agregar = 0
    return redirect('/listarAsesoria')

def salir(request):
    tipo = 0
    agregar = 0
    return render(request, 'registration/login.html')

def logout(request):
    request.session['id'] = ''
    return render(request, 'registration/login.html')
