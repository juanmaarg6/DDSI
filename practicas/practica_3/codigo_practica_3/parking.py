# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Subsistema: Parking (realizado por Juan Manuel Rodríguez Gómez)

from tabulate import tabulate   # py -m pip install tabulate (para presentar los datos en formato tabla)
import random                   # Instalado por defecto      (para números aleatorios en Python)
                                # Si no estuviese instalado: py -m pip install random

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
# Función para añadir una nueva reserva de una plaza del parking en la 
# tabla "ReservaParking"

def registrarReservaParking(cursor):

    # Establecemos aquí este savepoint de forma que si se ha 
    # introducido un DNI/Pasaporte incorrecto del cliente, 
    # al hacer rollback a este savepoint se deshace la inserción de 
    # la tupla de la nueva reserva a la tabla "ReservaParking"
    cursor.execute("SAVEPOINT DatosRegistrarReservaParking")

    # Elección aleatoria de una plaza disponible
    try:
        query_obtener_plazas_disponibles = "SELECT * FROM PlazaParking WHERE NumeroPlaza NOT IN (SELECT NumeroPlaza FROM ReservaParking)"
        cursor.execute(query_obtener_plazas_disponibles)
        tuplas_plazas_disponibles = cursor.fetchall()

        plazas_disponibles = [] # Lista donde cada elemento suyo será una plaza disponible

        for p in tuplas_plazas_disponibles:
            plazas_disponibles.append(p[0])
        
    except Exception as e:
        print('ERROR al CONSULTAR las PLAZAS DISPONIBLES DEL PARKING: ', e)
    
    # Si no hubiera plazas disponibles, no se puede hacer la reserva
    if(len(plazas_disponibles) == 0):
        print('\nNO HAY NINGUNA PLAZA DE PARKING DISPONIBLE')
    # Si hay plazas disponibles, se continua con la reserva
    else:
        # Inserción de la tupla de la reserva en la tabla "ReservaParking"
        try:
            NumeroPlaza = random.choice(plazas_disponibles)
            print('\nPlaza Disponible Seleccionada Aleatoriamente')
            DNI_Pasaporte_Cliente = input('Introduzca el DNI/Pasaporte del cliente: ')
            TiempoOcupacion = 0
            print('Tiempo de Ocupación establecido a 0 minutos')
        except ValueError as v:
            print('ERROR al INTRODUCIR los DATOS DE LA RESERVA DE LA PLAZA DE PARKING: ', v)

        query_agregar_reserva_parking = "INSERT INTO ReservaParking VALUES (" + str(NumeroPlaza) + ", '" + DNI_Pasaporte_Cliente + "', " + str(TiempoOcupacion) + ")"
        
        try:
            cursor.execute(query_agregar_reserva_parking)
        except Exception as e:
            print('\nERROR al INSERTAR TUPLA en la tabla "ReservaParking": ', e)
            return

        # Comprobación de que los datos de la nueva reserva están correctos.
        # En caso de que no estén correcto, se deshace la reserva
        print('Se ha añadido la siguiente reserva de plaza de parking: \
               \n NumeroPlaza: ' + str(NumeroPlaza) + ' \
               \n DNI/Pasaporte del Cliente: ' + DNI_Pasaporte_Cliente + ' \
               \n Tiempo de Ocupación Actual (en minutos): ' + str(TiempoOcupacion) + ' \
               ')

        guardar_cambios = ''

        while(guardar_cambios != 'S' and guardar_cambios != 'N'):
            guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

        if(guardar_cambios == 'N'):
            cursor.execute("ROLLBACK TO SAVEPOINT DatosRegistrarReservaParking")
            print("\nReserva de plaza de parking deshecha. Se debe realizar de nuevo la reserva, volviendo a introducir el DNI/Pasaporte del cliente")
        else:
            print("\nReserva de plaza de parking finalizada")

#########################################################################
# Función para consultar una reserva de una plaza de parking en la 
# tabla "ReservaParking"

def consultarReservaParking(cursor):
    try:
        DNI_Pasaporte_Cliente = input('Introduzca el DNI/Pasaporte del cliente: ')
    except ValueError as v:
        print('ERROR al INTRODUCIR el DNI/PASAPORTE DEL CLIENTE: ', v)

    query_consultar_reserva_parking = "SELECT * FROM ReservaParking WHERE DNI_Pasaporte = '" + DNI_Pasaporte_Cliente + "'"
    
    try:
        cursor.execute(query_consultar_reserva_parking)
        tupla_reserva_parking = cursor.fetchall()

        datos_reserva_parking = [] # Lista que contendra la tupla (en forma de lista) con los datos de la reserva de
                                   # la plaza de parking

        for r in tupla_reserva_parking:
            datos_reserva_parking.append(r)

        # Si no hubiera ninguna reserva asociada a dicho DNI/Pasaporte, se informa sobre ello
        if(len(datos_reserva_parking) == 0):
            print('\nNO HAY NINGUNA RESERVA DE PLAZA DE PARKING ASOCIADA AL DNI/PASAPORTE ' + DNI_Pasaporte_Cliente)
        # Si hay una reserva asociada a dicho DNI/Pasaporte, se muestran los datos de dicha reserva
        else:
            print('\nDatos de la reserva de la plaza de parking del cliente ' + str(datos_reserva_parking[0][1]) +':')
            print('\tNumero de Plaza: ' + str(datos_reserva_parking[0][0]))
            print('\tTiempo de Ocupación Actual (en minutos): ' + str(datos_reserva_parking[0][2]))
    except Exception as e:
        print('\nERROR al CONSULTAR TUPLA en la tabla "ReservaParking": ', e)

#########################################################################
# Función para consultar las plazas disponibles del Parking

def consultarPlazasDisponiblesParking(cursor):
    try:
        cursor.execute('SELECT NumeroPlaza FROM PlazaParking WHERE NumeroPlaza NOT IN (SELECT NumeroPlaza FROM ReservaParking)')
        tuplas_plazas_disponibles = cursor.fetchall()

        plazas_disponibles = [] # Lista donde cada elemento suyo será una plaza disponible

        for p in tuplas_plazas_disponibles:
            plazas_disponibles.append( [ p[0] ] )
        
        print('\nPlazas Disponibles en el Parking: \n')
        print(tabulate(plazas_disponibles, headers=["NumeroPlaza"], tablefmt='fancy_grid'))

    except Exception as e:
        print('ERROR al MOSTRAR las PLAZAS DISPONIBLES DEL PARKING: ', e)

#########################################################################
# Función para mostrar el precio a pagar de la reserva de la plaza
# de parking en función del tiempo que lleve ocupando el cliente
# dicha plaza.
# Devuelve el DNI/Pasaporte del cliente introducido para
# facilitar la operación de cancelar una reserva de una
# plaza del parking

def mostrarPrecioParking(cursor):

    # Consultamos el Tiempo de Ocupación del cliente en la plaza de parking que tiene reservada
    try:
        DNI_Pasaporte_Cliente = input('Introduzca el DNI/Pasaporte del cliente: ')
    except ValueError as v:
        print('ERROR al INTRODUCIR el DNI/PASAPORTE DEL CLIENTE: ', v)

    query_consultar_tiempo_parking = "SELECT TiempoOcupacion FROM ReservaParking WHERE DNI_Pasaporte = '" + DNI_Pasaporte_Cliente + "'"
    
    try:
        cursor.execute(query_consultar_tiempo_parking)
        tupla_reserva_parking = cursor.fetchall()

        tiempo_reserva_parking = [] # Lista que contendra el tiempo de ocupación asociado a una reserva de
                                   # una plaza de parking

        for r in tupla_reserva_parking:
            tiempo_reserva_parking.append(r[0])

        # Si no hubiera ninguna reserva asociada a dicho DNI/Pasaporte, se informa sobre ello
        if(len(tiempo_reserva_parking) == 0):
            print('\nNO HAY NINGUNA RESERVA DE PLAZA DE PARKING ASOCIADA AL DNI/PASAPORTE ' + DNI_Pasaporte_Cliente)
        # Si hay una reserva asociada a dicho DNI/Pasaporte, se muestran los datos de dicha reserva
        else:
            TiempoOcupacion = tiempo_reserva_parking[0]

            # En función del tiempo de ocupación, el cliente deberá pagar (o no) una cierta cantidad
            if (TiempoOcupacion <= 60):
                print('\nEl cliente NO TIENE QUE PAGAR NADA')
            else:
                PrecioParking = float( (TiempoOcupacion * 2)/100 )
                print('\nEl cliente TIENE QUE PAGAR: ' + str(PrecioParking) + '€')

    except Exception as e:
        print('\nERROR al CONSULTAR TUPLA en la tabla "ReservaParking": ', e)

    return DNI_Pasaporte_Cliente

#########################################################################
# Función para cancelar una reserva de una plaza del parking en la 
# tabla "ReservaParking"

def cancelarReservaParking(cursor):

    # Establecemos aquí este savepoint de forma que si se ha 
    # introducido un DNI/Pasaporte incorrecto del cliente, 
    # al hacer rollback a este savepoint se deshace la eliminación de 
    # la tupla de la reserva en la tabla "ReservaParking"
    cursor.execute("SAVEPOINT DatosCancelarReservaParking")

    DNI_Pasaporte_Cliente = mostrarPrecioParking(cursor)

    query_cancelar_reserva_parking = "DELETE FROM ReservaParking WHERE DNI_Pasaporte = '" + DNI_Pasaporte_Cliente + "'"

    try:
        cursor.execute(query_cancelar_reserva_parking)
    except Exception as e:
        print('\nERROR al ELIMINAR TUPLA en la tabla "ReservaParking": ', e)

    print('Se ha eliminado la reserva de plaza de parking del cliente: ' + DNI_Pasaporte_Cliente + ' ')

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        cursor.execute("ROLLBACK TO SAVEPOINT DatosCancelarReservaParking")
        print("\nCancelación de la reserva de la plaza de parking deshecha. Se debe realizar de nuevo la cancelación de la reserva, volviendo a introducir el DNI/Pasaporte del cliente")
    else:
        print('\Cancelación de la reserva de la plaza de parking del cliente ' + DNI_Pasaporte_Cliente + ' finalizada')


#########################################################################
# Menú con las diferentes opciones del subsistema Parking

def menuParking(cursor, connection):
    terminar = False

    while(not terminar):
        print("\n4.1) Registrar reserva de plaza de parking")
        print("4.2) Consultar reserva de plaza de parking")
        print("4.3) Consultar plazas disponibles del parking")
        print("4.4) Mostrar cantidad a pagar del parking")
        print("4.5) Cancelar reserva de plaza de parking")
        print("4.6) Volver al menú principal")

        option = pedirOpcion(6)

        match option:
            case 1:
                registrarReservaParking(cursor)
                connection.commit() # Hacemos los cambios permanentes en la base de datos
            case 2:
                consultarReservaParking(cursor)
            case 3:
                consultarPlazasDisponiblesParking(cursor)
            case 4:
                mostrarPrecioParking(cursor)
            case 5:
                cancelarReservaParking(cursor)
                connection.commit() # Hacemos los cambios permanentes en la base de datos
            case 6:
                terminar = True