# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Subsistema: Actividades de Ocio (realizado por Álvaro Rodríguez Gallardo)

from tabulate import tabulate   # py -m pip install tabulate (para presentar los datos en formato tabla)

#########################################################################
# Función para que el usuario introduzca una opción del menú

def pedirOpcion(n):
    num = 0
    while(num <= 0 or num > n):
        try:
            num = int(input("\nIntroduzca una opcion (Número entero entre 1 y " + str(n) +"): "))
        except ValueError as v:
            print('ERROR al procesar la OPCIÓN INTRODUCIDA: ', v)
     
    return num

#########################################################################
# Función para añadir una nueva actividad de ocio en la 
# tabla "ActividadOcio"

def RegistrarActividadOcio(cursor,connection):
    try:
        code = input("Introduzca el código de la nueva actividad: ")
        name = input("Introduzca el nombre de la actividad: ")
        description = input("Introduzca la descripción de la actividad: ")
        date = input("Introduzca la fecha en la que se realizará: ")
        hour = input("Introduzca la hora (hh:mm) en que se realizará: ")
        numPlaces = int(input("Introduzca la cantidad de plazas asociadas: "))
    except ValueError as v:
        print("ERROR al INTRODUCIR los DATOS DE LA ACTIVIDAD DE OCIO")

    query_add_activity = "INSERT INTO ActividadOcio VALUES ('"+code+"','"+name+"','"+description+"',TO_DATE('"+date+"','DD/MM/YYYY'),TO_DATE('"+hour+"','HH24:MI'),'"+str(numPlaces)+"')"

    try:
        cursor.execute(query_add_activity)
        connection.commit()
    except Exception as e:
        print('\nERROR al INSERTAR TUPLA en la tabla "ActividadOcio"',e)
        return

#########################################################################
# Función para añadir una nueva reserva de una actividad de ocio en la 
# tabla "ReservaAct"

def ReservarActividadOcio(cursor,connection):
    try:
        dni = input("Introduzca el DNI/Pasaporte de la persona a cuyo nombre está la reserva: ")
        code = input("Introduzca el código de la actividad: ")
        date = input("Introduzca la fecha en la que realizará la actividad: ")
        hour = input("Introduzca la hora (hh::mm) en la que realizará la actividad: ") 
        numPlaces = int(input("Introduzca el número de personas que realizarán la actividad: "))
    except Exception as e:
        print("\nERROR al INSERTAR los DATOS DE RESERVA")
        return

    query_consult_date = "SELECT Fecha FROM ActividadOcio WHERE Fecha=TO_DATE('"+date+"','DD/MM/YYYY') AND ActOcio='"+code+"'"
    query_consult_hour = "SELECT Hora FROM ActividadOcio WHERE Hora=TO_DATE('"+hour+"','HH24:MI') AND ActOcio='"+code+"'"
    query_add_booking = "INSERT INTO ReservaAct VALUES('"+dni+"','"+code+"',TO_DATE('"+date+"','DD/MM/YYYY'),TO_DATE('"+hour+"','HH24:MI'),'"+str(numPlaces)+"')"
    query_consult_places = "SELECT numPlazas FROM ActividadOcio WHERE ActOcio='"+code+"'"
    
    cursor.execute("SAVEPOINT NuevaReserva")

    try:
        cursor.execute(query_consult_date)
        MyDate = cursor.fetchone()
        cursor.execute(query_consult_hour)
        MyHour = cursor.fetchone()
        if(not MyDate):
            print("\nLa fecha introducida no está disponible para tal actividad. O no existe tal actividad")
            return
        elif(not MyHour):
            print("\nLa hora introducida no está disponible para tal actividad")
            return
        cursor.execute(query_consult_places)
        Previous = cursor.fetchone()
        After = int(Previous[0])-numPlaces
        query_update_places="UPDATE ActividadOcio SET NumPlazas='"+str(After)+"' WHERE ActOcio='"+code+"'" # Antes de introducir compruebo no es 0 con el disparador
        cursor.execute(query_update_places)
        cursor.execute(query_add_booking)

        guardar_cambios = ''

        while(guardar_cambios != 'S' and guardar_cambios != 'N'):
            guardar_cambios = input("¿Desea guardar el registro de la reserva de la actividad de ocio? [S/N]: ")

        if(guardar_cambios == 'N'):
            cursor.execute("ROLLBACK TO SAVEPOINT NuevaReserva")

        connection.commit()
    except Exception as e:
        print("\nError en la operación de añadido de reserva de una actividad", e)
        return

#########################################################################
# Función para consultar todas las actividades de ocio disponibles
# en una fecha dada

def ConsultarDisponibilidad(cursor):
    try:
        date = input("Introduzca la fecha en la que quiere hacer la consulta: ")
    except Exception as p:
        print("\nError en la introducción de la fecha para la consulta de disponibilidad: ", p)
        return

    print("\nA continuación se muestran todas las actividades disponibles para la fecha")
    try:
        query_consult_disponibility = "SELECT * FROM ActividadOcio WHERE Fecha=TO_DATE('"+date+"','DD/MM/YYYY')"
        cursor.execute(query_consult_disponibility)
        activities = cursor.fetchall()
        tuplas = []
        for s in activities:
            if (int(s[5]) > 0):
                tuplas.append([ s[0], s[1], s[2], s[3].strftime('%d/%m/%Y'),s[4].strftime('%H:%M'),s[5]])

        print(tabulate(tuplas,headers=["ActOcio", "Nombre","Descripcion","Fecha","Hora","NumPlazas"],tablefmt='fancy_grid'))

    except Exception as e:
        print("Error en la consulta de la tabla ActividadOcio,",e)
        return

#########################################################################
# Función para opinar sobre una actividad de ocio

def OpinarActividadOcio(cursor,connection):
    try:
        dni = input("Introduzca el DNI/Pasaporte del cliente: ")
        code = input("Introduzca el código de la actividad que quiere opinar: ")
        opinion = input("Introduzca su opinión: ")
        punt = -1
        while (punt<0 or punt>10):
            punt = int(input("Introduzca la puntuación (0-10): "))
    except Exception as a:
        print("\nError en la introducción de la opinión sobre una actividad",a)
        return
    
    query_add_opinion = "INSERT INTO OpinionAct VALUES ('"+dni+"','"+code+"','"+opinion+"','"+str(punt)+"')"

    cursor.execute("SAVEPOINT OpinionActividad")

    try:
        cursor.execute(query_add_opinion)

        guardar_cambios = ''

        while(guardar_cambios != 'S' and guardar_cambios != 'N'):
            guardar_cambios = input("¿Desea guardar la opinión introducida (no podrá ser eliminada)? [S/N]: ")

        if(guardar_cambios == 'N'):
            cursor.execute("ROLLBACK TO SAVEPOINT OpinionActividad")

        connection.commit()
    except Exception as e:
        print("\nError en la introducción de la tupla de opinión", e)
        return 

#########################################################################
# Función para consultar las opiniones de una actividad de ocio dada

def ConsultarOpiniones(cursor):
    try:
        code = input("Inserte el código de la actividad: ")
    except Exception as a:
        print("\nHa ocurrido un error en la inserción del código,",a)
        return

    try:
        query_consult_opinion = "SELECT * FROM OpinionAct WHERE ActOcio='"+code+"'"
        cursor.execute(query_consult_opinion)
        opinions = cursor.fetchall()

        tuplas = []

        for s in opinions:
            tuplas.append([s[1],s[2],s[3]])

        print(tabulate(tuplas,headers=["ActOcio","Opinion","Puntuacion"],tablefmt='fancy_grid'))
    except Exception as e:
        print("\nError en la consulta de opininones de una actividad,",e)
        return

#########################################################################
# Función para cancelar una reserva de una actividad de ocio en la 
# tabla "ReservaAct"

def CancelarReserva(cursor,connection):
    try:
        dni = input("Introduzca el DNI/Pasaporte del cliente que quiere eliminar la reserva: ")
        code = input("Introduzca el código de la actividad: ")
    except Exception as e:
        print("\nError en la introducción del DNI/Pasaporte para la eliminación de reserva ",e)
        return

    query_delete_row = "DELETE FROM ReservaAct WHERE DNI_Pasaporte='"+dni+"' AND ActOcio='"+code+"'"
    query_consult_places = "SELECT NumPlazas FROM ActividadOcio WHERE ActOcio='"+code+"'"
    query_consult_places_asociated = "SELECT NumPlazas FROM ReservaAct WHERE ActOcio='"+code+"' AND DNI_Pasaporte='"+dni+"'"

    cursor.execute("SAVEPOINT EliminarReserva")

    try:
        cursor.execute(query_consult_places)
        Before = cursor.fetchone()
        cursor.execute(query_consult_places_asociated)
        NumPeople = cursor.fetchone()
        After = int(Before[0]) + int(NumPeople[0])
        query_update_more_places = "UPDATE ActividadOcio SET NumPlazas='"+str(After)+"' WHERE ActOcio='"+code+"'"
        cursor.execute(query_update_more_places)
        cursor.execute(query_delete_row)

        guardar_cambios = ''

        while(guardar_cambios != 'S' and guardar_cambios != 'N'):
            guardar_cambios = input("¿Desea guardar los cambiós de la eliminación de la reserva introducida? [S/N]: ")

        if(guardar_cambios == 'N'):
            cursor.execute("ROLLBACK TO SAVEPOINT EliminarReserva")

        connection.commit()
    except Exception as a:
        print("\nError en la eliminación de reserva ",a)
        return 

#########################################################################
# Menú con las diferentes opciones del subsistema Actividades de Ocio

def menuActividadesOcio(cursor, connection):
    end = False

    while(not end):
        print('\n3.1) Registrar una actividad de ocio')
        print('3.2) Reservar una actividad de ocio')
        print('3.3) Consultar disponibilidad de una actividad de ocio')
        print('3.4) Opinar sobre una actividad de ocio')
        print('3.5) Consultar opiniones de una actividad de ocio')
        print('3.6) Cancelar reserva de una actividad de ocio')
        print('3.7) Volver al menú principal')

        option = pedirOpcion(7)

        match option:
            case 1:
                RegistrarActividadOcio(cursor, connection)
            case 2:
                ReservarActividadOcio(cursor, connection)
            case 3:
                ConsultarDisponibilidad(cursor)
            case 4:
                OpinarActividadOcio(cursor, connection)
            case 5:
                ConsultarOpiniones(cursor)
            case 6:
                CancelarReserva(cursor, connection)
            case 7:
                end = True
