from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User
from asesorias.models import Asesoria, Curso, Seccion, FactTable, Cita
from django.http import JsonResponse
import json
import cloudinary.api
import cloudinary.uploader
from django.template.loader import render_to_string
from datetime import date, timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

# credenciales para usar cloudinary
cloudinary.config(
  cloud_name = "dcmdp3lbl",
  api_key = "322921397444291",
  api_secret = "cYxPSGxHfzbGqA3UK6QcBKShChw"
)

def mostrarFechas(year,dia):
    arrFechas=[]
    dt = date(year, 8, 13)# inicio de conteo de fechas
    #dt = date(13, 8, year)
    dt += timedelta(days = dia - dt.weekday())
    while dt.year == year:
      #yield dt
      arrFechas.append(dt)
      dt += timedelta(days = 7)
    return arrFechas

def index(request):
    tipo = 0
    agregar = 0
    return render(request, 'registration/login.html')

def login2(request):
    return render(request, 'registration/login2.php')

def registro(request):
    return render(request, 'registration/registro.html')

def register(request):
    a=request.POST['last_name']
    errors = User.objects.validator(request.POST)
    #print(len(errors))
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/registro')

    #hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    hashed_password = request.POST['password']
    tipoUsuario=request.POST['tipoUsuario']
    is_profesor=False
    is_estudiante=False
    is_admin=False
    if tipoUsuario == "profesor":
        is_profesor= True
    elif tipoUsuario == "estudiante":
        is_estudiante= True
    else:
        is_admin=True

    user = User.objects.create(is_profesor=is_profesor,is_estudiante=is_estudiante,is_admin=is_admin,first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/')

def login(request):
    mensaje=""
    mensaje2=""
    if (User.objects.filter(email=request.POST['login_email']).exists()):
        user = User.objects.filter(email=request.POST['login_email'])[0]

        #if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):
        if request.POST['login_password'] == user.password:
            request.session['id'] = user.id
            agregar = 0
            tipo = 0
            if user.is_admin== True:
                return redirect('/listarAsesoria')

            elif user.is_estudiante== True:
                return redirect('/alumnoVista')

            elif user.is_profesor == True:
                return redirect( '/profesorVista')
        else:
            mensaje="Contraseña incorrecta"
            return render(request, 'registration/login.html', locals())
    else:
        mensaje="Correo incorrecto"
        return render(request, 'registration/login.html', locals())
def vistaProfesor(request):

    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']
    cita= Cita.objects.all().order_by('id')
    cursoProfe= FactTable.objects.filter(profesor_id=id_profesor)
    arregloC=[]
    arregloCurso=[]
    cursoInfo={}
    for fact in cursoProfe:
        id_curso= fact.curso_id
        nombreCurso= Curso.objects.filter(id=fact.curso_id)
        for cursillo in nombreCurso:
            arregloC.append(cursillo)
            arregloCurso=quitarDup(arregloC)

    for z in cita:
        if (z.estado == True):
            x_info = {}
            x_info['id']= z.id
            alumno= User.objects.get(id=z.alumno_id)
            x_info['alumno']= alumno.first_name
            x_info['comentario']= z.comentario
            x_info['fechaCita'] = z.fechaCita
            result = cloudinary.Search().expression('public_id:'+z.archivo+'').execute()
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']
            factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

            for x in factTable:

                if (x.profesor_id == id_profesor):
                    #CURSO
                    curso= Curso.objects.filter(id=x.curso_id)
                    for y in curso:
                        x_info['curso'] = y.nombre

                    #ASESORIA
                    asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                    for y in asesoria:

                        x_info['horario'] = y.horario
                        x_info['dia'] = y.dia
                        x_info['lugar'] = y.lugar

                    #Seccion
                    seccion=Seccion.objects.filter(id=x.seccion_id)
                    for y in seccion:
                        x_info['seccion'] = y.codigo

                    arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'profesorVista.html', locals())

def vistaAlumno(request):
    tipo = 0
    agregar = 0
    factTable = FactTable.objects.all().order_by("id")
    print(factTable)
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    for x in factTable:
        print (5)
        x_info = {}

        #CURSO
        curso= Curso.objects.filter(id=x.curso_id)
        for y in curso:
            x_info['curso'] = y.nombre

        #PROFESOR
        profesor=User.objects.filter(id=x.profesor_id)
        for y in profesor:
            x_info['profesor'] = y.first_name+" "+y.last_name

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
    #print(arreglo)

    return render(request, 'alumnoVista.html', locals())
def alumnoCitaError(request):
    tipo = 0
    agregar = 0
    if (request.session['validate'] == 1):
        if (Cita.objects.filter(fechaCita=request.session['fecha_pactada'], asesoria_id=request.session['id_asesoria'], suspendido=True).exists()):
            errorFecha=1
    elif (request.session['validate'] == 0):
        errorFecha=0
    factTable = FactTable.objects.all().order_by("id")
    print(factTable)
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    for x in factTable:
        print (5)
        x_info = {}

        #CURSO
        curso= Curso.objects.filter(id=x.curso_id)
        for y in curso:
            x_info['curso'] = y.nombre

        #PROFESOR
        profesor=User.objects.filter(id=x.profesor_id)
        for y in profesor:
            x_info['profesor'] = y.first_name+" "+y.last_name

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
    #print(arreglo)

    return render(request, 'alumnoVista.html', locals())

def uploadFiles(idCita,file):

    nomFile=str(file)
    nomFin=str(idCita)+','+nomFile
    u=cloudinary.uploader.upload(file,resource_type="raw", public_id= nomFin )# uso del api de cloudinary
    url=u['url']
    result = cloudinary.Search().expression('public_id='+nomFin+'').execute()
    return nomFin
def crearCita(alumno,asesoria,comentario,estado,fechaCita):
    cita= Cita.objects.create(alumno_id= alumno, asesoria_id=asesoria,comentario=comentario, estado=estado,fechaCita=fechaCita)
    cita.save()
    return True
def generarCita(request):
    arrFechas=[]
    arrFechas=mostrarFechas(2018,0)
    val=request.POST['fecha_pactada']
    for s in arrFechas:
       print(s)
    file=request.FILES['file'] if 'file' in request.FILES else False
    if (Cita.objects.filter(fechaCita=request.POST['fecha_pactada'], asesoria_id=request.POST['id_asesoria'], suspendido=True).exists()):
        #si es que existe una cita suspendida
        request.session['fecha_pactada']=request.POST['fecha_pactada']
        request.session['id_asesoria']=request.POST['id_asesoria']
        request.session['validate'] = 1
        return redirect('/alumnoCitaError')

    elif (Cita.objects.filter(alumno_id=request.session['id'],fechaCita=request.POST['fecha_pactada'], asesoria_id=request.POST['id_asesoria'], estado=True).exists()):
        request.session['validate'] = 0
        errorFecha=0
        return redirect('/alumnoCitaError')
    else:
        #cita= Cita.objects.create(alumno_id= request.session['id'], asesoria_id=request.POST['id_asesoria'],comentario=request.POST['comentario'], estado=True,fechaCita=val)
        #cita.save()
        crearCita(request.session['id'],request.POST['id_asesoria'],request.POST['comentario'],True,val)
    if file==False:# si es que no hay archivo
        print("No se grabo")
    else:
        cita.archivo=uploadFiles(cita.id,file)
        cita.save()
    return redirect('/alumnoCita')

def consultarCita(request):
    return redirect('/alumnoCita')

def alumnoCita(request):
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    id_alumno = request.session['id']
    cita= Cita.objects.filter(alumno_id= id_alumno)

    for x in cita:
        if (x.estado == True):
            x_info = {}
            x_info['id'] = x.id
            x_info['comentario'] = x.comentario
            x_info['fechaCita'] = x.fechaCita
            result = cloudinary.Search().expression('public_id:'+x.archivo+'').execute()
            print("LEEEN")
            print(result["total_count"])
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']
            #ASESORIA
            asesoria=Asesoria.objects.filter(id=x.asesoria_id)
            for y in asesoria:
                x_info['horario'] = y.horario
                x_info['dia'] = y.dia
                x_info['lugar'] = y.lugar

                factTable = FactTable.objects.filter(asesoria_id= y.id)

                for fact in factTable:

                    #CURSO
                    curso= Curso.objects.filter(id=fact.curso_id)
                    for q in curso:
                        x_info['curso'] = q.nombre

                    #PROFESOR
                    profesor=User.objects.filter(id=fact.profesor_id)
                    for q in profesor:
                        x_info['profesor'] = q.first_name+" "+q.last_name

                    #Seccion
                    seccion=Seccion.objects.filter(id=fact.seccion_id)
                    for q in seccion:
                        x_info['seccion'] = q.codigo

            arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'alumnoCita.html', locals())


def regresar(request):
    return redirect('/alumnoVista')

def cancelarCita(request):
    id=request.POST.get('id_cita', False)
    Cita.objects.filter(id=id).delete()
    return redirect('/alumnoCita')

def marcarAtencion(request):
    id_cita=request.POST.get('id_cita', False)
    print(id_cita)
    cita= Cita.objects.get(id=id_cita)
    #print(cita)
    cita.estado = False
    cita.save()
    return redirect('/profesorVista')
def buscar(request):
    busqueda=request.POST['buscar']
    print(request)
    buscarCurso=Curso.objects.filter(nombre__iexact=busqueda)
    buscarProfesor=User.objects.filter(first_name__iexact=busqueda)
    buscarProfesor2=User.objects.filter(last_name__iexact=busqueda)
    buscarHorario=Asesoria.objects.filter(horario__iexact=busqueda)
    buscarDia=Asesoria.objects.filter(dia__iexact=busqueda)
    buscarLugar=Asesoria.objects.filter(lugar__iexact=busqueda)
    buscarSeccion=Seccion.objects.filter(codigo__iexact=busqueda)

    #Buscar si es curso
    if buscarCurso:
        id= Curso.objects.get(nombre__iexact=busqueda)
        factTable=FactTable.objects.filter(curso_id=id.id)

    #Buscar si es Profesor
    elif buscarProfesor:
        id= User.objects.get(first_name__iexact=busqueda)
        factTable=FactTable.objects.filter(profesor_id=id.id)

    elif buscarProfesor2:
        id= User.objects.get(last_name__iexact=busqueda)
        factTable=FactTable.objects.filter(profesor_id=id.id)

    #Buscar si es Horario
    elif buscarHorario:
        id= Asesoria.objects.get(horario__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Dia
    elif buscarDia:
        id= Asesoria.objects.get(dia__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Lugar
    elif buscarLugar:
        id= Asesoria.objects.get(lugar__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Seccion
    elif buscarSeccion:
        id= Seccion.objects.get(codigo__iexact=busqueda)
        factTable=FactTable.objects.filter(seccion_id=id.id)

    else:
        factTable=FactTable.objects.filter(curso_id=99999)

    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
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
    #print(arreglo)||||||

    return render(request, 'alumnoVista.html', locals())
def quitarDup(a):
    dup_items = set()
    uniq_items = []

    for x in a:
        print(x.id)
        if x.id not in dup_items:
            uniq_items.append(x)
            dup_items.add(x.id)
    return uniq_items



def validate_curso(request):
    curso = request.GET.get('curso', None)
    buscarCurso=Curso.objects.filter(nombre__iexact=curso)
    objCurso= Curso.objects.get(nombre__iexact=curso)
    factTable=FactTable.objects.filter(curso_id=objCurso.id)
    print(curso)
    print(buscarCurso)
    print(id)
    print(factTable)
    temp=[]
    profes=[]
    Cursos=[]
    print()
    profesor=[]
    Secciones=[]
    arr=[]
    Secciones=Seccion.objects.filter(curso=objCurso)
    print("LEN SECCIONESs")
    print(len(Secciones))
    for i in Secciones:
        profesor.append(i.profesor)
        for y in profesor:
            temp.append(y)
            arr=quitarDup(temp)
    for i in arr:
        profes.append(i.first_name + " " + i.last_name)
    data = {
        'is_taken' : True,
        'profesores' : json.dumps(profes)
    }
    return JsonResponse(data)

def validate_profesor(request):
    first = request.GET.get('first', None)
    last=request.GET.get('last',None)
    curso=request.GET.get('curso',None)
    id=User.objects.get(first_name__iexact=first)
    id2=User.objects.get(last_name__iexact=last)
    curso=Curso.objects.get(nombre__iexact=curso)
    factTable=FactTable.objects.filter(profesor_id=id.id)
    temp=[]
    secciones=[]
    Secciones=Seccion.objects.filter(profesor=id,curso=curso)
    if id.id==id2.id:
        for y in Secciones:
            print(y.codigo)
            temp.append(y)
            arr=quitarDup(temp)

        for i in arr:
            secciones.append(i.codigo)

    data = {
        'is_taken' : True,
        'seccion' : json.dumps(secciones)
    }
    return JsonResponse(data)


def citaAtendida(request):
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    id_alumno = request.session['id']
    cita= Cita.objects.filter(alumno_id= id_alumno)
    expresion= "null"
    for x in cita:
        if (x.estado == False):
            x_info = {}
            x_info['id'] = x.id
            x_info['comentario'] = x.comentario
            x_info['feedback'] = x.feedback
            #ASESORIA
            asesoria=Asesoria.objects.filter(id=x.asesoria_id)
            for y in asesoria:
                x_info['horario'] = y.horario
                x_info['dia'] = y.dia
                x_info['lugar'] = y.lugar

                factTable = FactTable.objects.filter(asesoria_id= y.id)

                for fact in factTable:

                    #CURSO
                    curso= Curso.objects.filter(id=fact.curso_id)
                    for q in curso:
                        x_info['curso'] = q.nombre

                    #PROFESOR
                    profesor=User.objects.filter(id=fact.profesor_id)
                    for q in profesor:
                        x_info['profesor'] = q.first_name+" "+q.last_name

                    #Seccion
                    seccion=Seccion.objects.filter(id=fact.seccion_id)
                    for q in seccion:
                        x_info['seccion'] = q.codigo

            arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'citaAtendida.html', locals())

def feedback(request):
    feedback = request.POST['feedback']
    id_cita=request.POST.get('id_cita', False)
    cita= Cita.objects.get(id=id_cita)
    cita.feedback= feedback
    cita.estado = False
    cita.save()
    return redirect('/profesorVista')

def citaFin(request):
    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']
    cita=Cita.objects.filter(suspendido=False)
    expresion= "null"
    for z in cita:
        if (z.estado == False):
            x_info = {}
            x_info['id']= z.id
            alumno= User.objects.get(id=z.alumno_id)
            x_info['alumno']= alumno.first_name
            x_info['comentario']= z.comentario
            x_info['feedback']= z.feedback
            x_info['fechaCita']=z.fechaCita

            result = cloudinary.Search().expression('public_id:'+z.archivo+'').execute()
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']

            factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

            for x in factTable:

                if (x.profesor_id == id_profesor):
                    #CURSO
                    curso= Curso.objects.filter(id=x.curso_id)
                    for y in curso:
                        x_info['curso'] = y.nombre

                    #ASESORIA
                    asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                    for y in asesoria:

                        x_info['horario'] = y.horario
                        x_info['dia'] = y.dia
                        x_info['lugar'] = y.lugar

                    #Seccion
                    seccion=Seccion.objects.filter(id=x.seccion_id)
                    for y in seccion:
                        x_info['seccion'] = y.codigo

                    arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'citaFin.html', locals())


def obtenerFechaCita(request):
    numSemana = request.GET.get('numSemana', None)
    idSemana = request.GET.get('idSemana', None)
    diaSemana = request.GET.get('diaSemana', None)
    switcher = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6,
    }
    numDia=switcher[diaSemana]

    arrSepId=[]
    arrSepNum=[]
    arrSepId=idSemana.split("/")
    arrSepNum=numSemana.split("/")
    arrFechas=[]
    arrFechas=mostrarFechas(2018,numDia)
    semanaElegida=arrSepNum[1]
    fecha=arrFechas[int(semanaElegida)-1]
    print("FECHAAA")
    print(fecha)
    data = {
        'is_taken' : True,
        'fecha' : fecha
    }
    return JsonResponse(data)

def regresarVistaProfe(request):
    return redirect('/profesorVista')

def validate_dia(request):
    curso = request.GET.get('curso', None)
    buscarCurso=Curso.objects.filter(nombre__iexact=curso)
    objCurso= Curso.objects.get(id=curso)
    factTable=FactTable.objects.filter(curso=objCurso)
    objProf= User.objects.get(id=request.session['id'])
    temp=[]
    Secciones=[]
    arr=[]
    asesoriaArr=[]
    dias=[]
    Secciones=Seccion.objects.filter(curso=objCurso, profesor=objProf)
    print("LEN SECCIONESs")
    print(len(Secciones))
    for i in Secciones:
        asesoriaArr=Asesoria.objects.filter(seccion=i)
        for y in asesoriaArr:
            temp.append(y)
            arr=quitarDup(temp)
    for i in arr:
        dias.append(i.dia)

    #print(len(profes))
    data = {
        'is_taken' : True,
        'dias' : json.dumps(dias)
    }
    return JsonResponse(data)


def cancelarAsesoria(request):
    curso= request.POST['cursoSeleccionado']
    semana= request.POST['semanaSeleccionada']
    dia= request.POST['diaSeleccionado']
    id_profesor = request.session['id']
    curso= int(curso)
    semana= int(semana)
    fact=FactTable.objects.filter(curso_id=curso)
    arregloA=[]
    arregloAsesorias=[]

    for i in fact:
        asesoria= Asesoria.objects.filter(id=i.id)
        for y in asesoria:
            arregloA.append(y)
            arregloAsesorias=quitarDup(arregloA)

    switcher = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6,
    }
    numDia=switcher[dia]
    arrFechas=[]
    arrFechas=mostrarFechas(2018,numDia)
    fecha=arrFechas[semana-1]
    for i in arregloAsesorias:
        cita=Cita.objects.filter(asesoria_id=i.id)
        for y in cita:
            t=y.fechaCita
            #print(t.strftime('%Y-%m-%d'))
            #print(fecha)
            if (str(t.strftime('%Y-%m-%d'))==str(fecha)):
                y.delete()
            else:
                print('NO PASAA ')

    return redirect('/profesorVista')

def cambiarDisponibilidad(request):
    curso= request.POST['cursoSeleccionado2']
    semana= request.POST['semanaSeleccionada2']
    dia= request.POST['diaSeleccionado2']
    id_profesor = request.session['id']
    curso= int(curso)
    semana= int(semana)
    nombreProfesor = User.objects.get(id=request.session['id'])
    objCurso= Curso.objects.get(id=curso)
    print(objCurso)
    Secciones=[]
    Secciones=Seccion.objects.filter(profesor=nombreProfesor,curso=objCurso)

    asesoriaArr=[]
    CitasArr=[]

    for i in Secciones:
        asesoriaArr=Asesoria.objects.filter(seccion=i, dia=dia)
        for y in asesoriaArr:
            CitasArr=Cita.objects.filter(asesoria=y)
            for z in CitasArr:
                asesoria_id= z.asesoria_id
    #seccion=Seccion.objects.filter(curso_id=curso, profesor_id=id_profesor)
    #asesoria=Asesoria.objects.filter(seccion_id=seccion.id)


    switcher = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6,
    }
    numDia=switcher[dia]
    arrFechas=[]
    arrFechas=mostrarFechas(2018,numDia)
    fecha=arrFechas[semana-1]

    cita= Cita.objects.create(alumno_id= request.session['id'], asesoria_id=asesoria_id ,comentario="-", estado=False,fechaCita=fecha, suspendido=True)
    cita.save()
    return redirect('/profesorVista')

@csrf_exempt
def busquedaProfesor(request):
    busqueda=request.POST['buscar']
    print(request)

    buscarAlumno=[]
    buscarAlumno2=[]
    buscarHorario=[]#no necesario
    buscarDia=[]
    buscarLugar=[]#no necesario
    buscarSeccion=[]
    arreglo=[]
    buscarCurso=Curso.objects.filter(nombre__iexact=busqueda)
    buscarAlumno=User.objects.filter(first_name__iexact=busqueda)
    buscarAlumno2=User.objects.filter(last_name__iexact=busqueda)
    buscarHorario=Asesoria.objects.filter(horario__iexact=busqueda)
    buscarDia=Asesoria.objects.filter(dia__iexact=busqueda)
    buscarLugar=Asesoria.objects.filter(lugar__iexact=busqueda)
    buscarSeccion=Seccion.objects.filter(codigo__iexact=busqueda)
    print(buscarCurso)
    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']

    #Buscar si es curso
    if buscarCurso:
        print("buscoo crusas")
        Cursos= Curso.objects.get(nombre__iexact=busqueda)#se obtiene el objeto curso
        Secciones=Seccion.objects.filter(profesor=nombreProfesor,curso=Cursos)#Se obtienen las secciones del curso que son del profesor
        asesoriaArr=[]
        CitasArr=[]
        print(Secciones[0])

        for i in Secciones:
            asesoriaArr=Asesoria.objects.filter(seccion=i)
            for y in asesoriaArr:
                CitasArr=Cita.objects.filter(asesoria=y)
                for z in CitasArr:
                    if (z.estado == False and z.suspendido==False):
                        x_info = {}
                        x_info['id']= z.id
                        alumno= User.objects.get(id=z.alumno_id)
                        x_info['alumno']= alumno.first_name
                        x_info['comentario']= z.comentario
                        x_info['seccion']= i.codigo
                        x_info['fechaCita']= z.fechaCita
                        x_info['feedback']= z.feedback
                        factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

                        for x in factTable:
                            if (x.profesor_id == id_profesor):
                                #CURSO
                                curso= Curso.objects.filter(id=x.curso_id)
                                for m in curso:
                                    x_info['curso'] = m.nombre
                                    #ASESORIA
                                asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                                for w in asesoria:
                                    x_info['horario'] = w.horario
                                    x_info['dia'] = w.dia
                                    x_info['lugar'] = w.lugar
                                    arreglo.append(x_info)
    #Buscar si es Alumno
    elif buscarAlumno:
        alumnoObj=[]
        CitasArr=[]
        print("ya nonononon")
        alumnoObj= User.objects.filter(first_name__iexact=busqueda)
        for i in alumnoObj:

            CitasArr=Cita.objects.filter(alumno=i)

            for z in CitasArr:

                x_info = {}
                x_info['id']= z.id
                alumno= User.objects.get(id=z.alumno_id)
                x_info['alumno']= alumno.first_name
                x_info['comentario']= z.comentario

                x_info['fechaCita']= z.fechaCita
                x_info['feedback']= z.feedback
                factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

                for x in factTable:

                    if (x.profesor_id == id_profesor):
                        #CURSO
                        curso= Curso.objects.filter(id=x.curso_id)
                        for y in curso:
                            x_info['curso'] = y.nombre
                            #ASESORIA
                        asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                        for y in asesoria:
                            x_info['seccion'] = y.seccion
                            x_info['horario'] = y.horario
                            x_info['dia'] = y.dia
                            x_info['lugar'] = y.lugar
                            arreglo.append(x_info)

    elif buscarAlumno2:
        id= User.objects.get(last_name__iexact=busqueda)
        factTable=FactTable.objects.filter(profesor_id=id.id)

    #Buscar si es Horario
    elif buscarHorario:
        id= Asesoria.objects.get(horario__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Dia
    elif buscarDia:
        id= Asesoria.objects.get(dia__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Lugar
    elif buscarLugar:
        id= Asesoria.objects.get(lugar__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Seccion
    elif buscarSeccion:
        id= Seccion.objects.get(codigo__iexact=busqueda)
        factTable=FactTable.objects.filter(seccion_id=id.id)

    else:
        factTable=FactTable.objects.filter(curso_id=99999)


    nombreAlumno = User.objects.get(id=request.session['id'])

    #print(arreglo)||||||

    return render(request, 'citaFin.html', locals())

@csrf_exempt
def ordCitasFin(request):
    print("llego")
    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']
    tipoOrd= request.POST.get('tipoOrd', None)

    print(tipoOrd)
    print(id_profesor)
    print("sssssssss")
    cita=Cita.objects.filter(suspendido=False)
    expresion= "null"
    for z in cita:
        if (z.estado == False):
            x_info = {}
            x_info['id']= z.id
            alumno= User.objects.get(id=z.alumno_id)
            x_info['alumno']= alumno.first_name
            x_info['comentario']= z.comentario
            x_info['feedback']= z.feedback
            x_info['fechaCita']=z.fechaCita
            result = cloudinary.Search().expression('public_id:'+z.archivo+'').execute()
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']
            factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)
            for x in factTable:
                if (x.profesor_id == id_profesor):
                    #CURSO
                    print("paso el orden ")
                    curso= Curso.objects.filter(id=x.curso_id)
                    for y in curso:
                        x_info['curso'] = y.nombre
                    #ASESORIA
                    asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                    for y in asesoria:

                        x_info['horario'] = y.horario
                        x_info['dia'] = y.dia
                        x_info['lugar'] = y.lugar

                    #Seccion
                    seccion=Seccion.objects.filter(id=x.seccion_id)
                    for y in seccion:
                        x_info['seccion'] = y.codigo

                    arreglo.append(x_info)
    if tipoOrd=="-" or tipoOrd=="asc":
        arrOrd = sorted(arreglo, key=lambda k: k['fechaCita'],reverse=True)
    elif tipoOrd=="desc":
        arrOrd = sorted(arreglo, key=lambda k: k['fechaCita'])
    arreglo=arrOrd
    if request.is_ajax():
        html = render_to_string('citaFinOrd.html', locals())
        return HttpResponse(html)

    return render(request, 'citaFin.html', local())
