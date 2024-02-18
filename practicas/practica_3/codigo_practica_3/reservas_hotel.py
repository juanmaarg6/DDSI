# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Subsistema: Reservas del Hotel (realizado por Alejandro Cárdenas Barranco)

from datetime import *          # Instalado por defecto      (para fechas en Python)
                                # Si no estuviese instalado: py -m pip install datetime
import string                   # Instalado por defecto      (para cadenas de caracteres en Python)
                                # Si no estuviese instalado: py -m pip install string
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
# Función para crear aleatoriamente un id de reserva

def idReserva(): 
  # Generamos una lista con todas las letras del alfabeto y los dígitos del 0 al 9
  characters = string.ascii_letters + string.digits
  # Generamos una lista con 9 caracteres aleatorios
  random_characters = [random.choice(characters) for _ in range(9)]
  # Añadimos al principio de la lista la letra "R"
  random_characters.insert(0, "R")
  # Devolvemos la lista como una cadena de caracteres
  return "".join(random_characters)

#########################################################################
# Función que , dado un tipo de habitación, se mostrará una lista con 
# todas las habitaciones disponibles del tipo "individual,doble o suite".
# Si el tipo introducido no coincide con ninguno, se mostrarán todas 
# las habitaciones disponibles (sin importar el tipo)

def habitaciones_disponibles(cursor,tipo): 
    tipo = tipo.lower()
    print(tipo)
    if (tipo == "individual" or tipo == "doble" or tipo == "suite"): 
        query_habitaciones_de_un_tipo_no_ocupadas = "SELECT NumeroHabitacion FROM Habitacion \
                                                  WHERE LOWER(TipoHabitacion)='"+tipo+"' AND \
                                                  NumeroHabitacion NOT IN (SELECT NumeroHabitacion FROM HabReserva)"
        try:
            cursor.execute(query_habitaciones_de_un_tipo_no_ocupadas)
            return cursor.fetchall()
        except Exception as e:
            print('ERROR al leer la tabla Habitacion": ', e)
            return
    else: #Si el tipo es distinto de los otros 3 dará una lista con todas las habitaciones disponibles
        print(tipo)
        query_habitaciones_de_un_tipo_no_ocupadas = "SELECT NumeroHabitacion FROM Habitacion \
                                                  WHERE NumeroHabitacion NOT IN (SELECT NumeroHabitacion FROM HabReserva)"
        cursor.execute(query_habitaciones_de_un_tipo_no_ocupadas)
        return cursor.fetchall()
        

#########################################################################
# Función para añadir una nueva reserva del hotel

def registrarReserva(cursor, connection):

    cursor.execute("SAVEPOINT DatosRegistrarReserva")

    #Cliente
    dni = input('Introduzca el DNI o Pasaporte del cliente que quiere registrar una reserva: ')
    cuentaBancaria = input('Introduzca la cuenta bancaria del cliente que quiere registrar una reserva: ')
    telefono = input('Introduzca el telefono del cliente que quiere registrar una reserva: ')


    tipoHabitacion = input('Introduzca el tipo de habitación que quiere resevar (individual, doble o suite) Un tipo diferente a esto se considerará que no hay preferencia: ')
    tipoHabitacion=tipoHabitacion.lower() #Lo pasamos a minúsculas

    fecha_entrada = input('Introduzca la fecha de entrada (dd/mm/yyyy): ')
    fecha_salida = input('Introduzca la fecha de salida (dd/mm/yyyy): ')

    try:
        fechaE =  datetime.strptime(fecha_entrada, '%d/%m/%Y')
        fechaS =  datetime.strptime(fecha_salida, '%d/%m/%Y')
    except Exception as e:
        print("Fecha Introducida incorrectamente, inténtelo de nuevo")
        return


    #Primero contamos cuantas habitaciones individuales, suites y dobles hay en total en el hotel.

    query_contar_individuales = "SELECT COUNT(*) FROM Habitacion WHERE LOWER(TipoHabitacion)='individual'"
    query_contar_dobles = "SELECT COUNT(*) FROM Habitacion WHERE LOWER(TipoHabitacion)='doble'" 
    query_contar_suites = "SELECT COUNT(*) FROM Habitacion WHERE LOWER(TipoHabitacion)='suite'"


    try:
        cursor.execute(query_contar_individuales)
        num_individuales = cursor.fetchone()[0]

        cursor.execute(query_contar_dobles)
        num_dobles = cursor.fetchone()[0]

        cursor.execute(query_contar_suites)
        num_suites = cursor.fetchone()[0]

        dia = fechaE
        
        #Tenemos que comprobar que hay habitaciones libres del tipo indicado en este rango de fechas

        #Para ello, por cada día contaremos cuántas habitaciones libres hay del tipo especifico, si en uno de los días quedan 0, no podrá efectuarse la reserv

        
        if (tipoHabitacion=="individual" or tipoHabitacion=="suite" or tipoHabitacion=="doble"):
        #Primero contamos cuantas habitaciones individuales, suites y dobles hay en total en el hotel.
            while(dia<=fechaS):
                query_contar_hab_ocupadas = "SELECT COUNT(*) FROM ReservaHotel WHERE LOWER(TipoHabitacionPedida) = '" + tipoHabitacion +"' AND  FechaEntrada <= TO_DATE('" + dia.strftime("%d/%m/%y") + "','DD/MM/YY') AND FechaSalida>= TO_DATE('" + dia.strftime("%d/%m/%y") + "','DD/MM/YY')"
                cursor.execute(query_contar_hab_ocupadas)
                for i in cursor:
                    hab_ocupadas= i[0]
                if ( (tipoHabitacion == "individual" and (num_individuales-hab_ocupadas)<=0)  or (tipoHabitacion == "doble" and (num_dobles-hab_ocupadas)<=0) or (tipoHabitacion == "suite" and (num_suites-hab_ocupadas)<=0)):
                    print("No es posible efectuar la reserva, no quedan habitaciones libres")
                    return
                dia = dia + timedelta(days=1)
        else: #No importa si es individual suite o doble
            num_total_hab = num_suites+num_dobles+num_individuales
            while(dia<=fechaS):
                query_contar_hab_ocupadas = "SELECT COUNT(*) FROM ReservaHotel WHERE FechaEntrada <= TO_DATE('" + dia.strftime("%d/%m/%y") + "','DD/MM/YY') AND FechaSalida>= TO_DATE('" + dia.strftime("%d/%m/%y") + "','DD/MM/YY')"
                cursor.execute(query_contar_hab_ocupadas)
                for i in cursor:
                    hab_ocupadas= i[0]
                if(num_total_hab-hab_ocupadas<=0):
                    print("No es posible efectuar la reserva, no quedan habitaciones libres")
                    return
                dia = dia + timedelta(days=1)
    except Exception as e:
        print("Error al comprobar que si hay habitaciones libres")
        return    

    #Creamos de manera aleatoria el id de la reserva

    id_reserva = idReserva()

    #comprobamos que no se repita (aunque las probabilidades son prácticamente 0)
    try:
        cursor.execute("SELECT * FROM ReservaHotel WHERE CReserva = '" + id_reserva + "'")
        reserva_mismoId = cursor.fetchone()
        while(reserva_mismoId):
            id_reserva = idReserva()
            cursor.execute("SELECT * FROM ReservaHotel WHERE CReserva = '" + id_reserva + "'")
            reserva_mismoId = cursor.fetchone()
    except Exception as e:
        print("Error al intentar crear el ID de la reserva, inténtelo de nuevo")
        return


    query_agregar_tupla_clientes = "INSERT INTO Cliente VALUES ('" + dni + "','" + telefono + "', '" + cuentaBancaria + "')"
    query_agregar_tupla_reserva = "INSERT INTO ReservaHotel VALUES ('" + id_reserva + "', TO_DATE('" + fecha_entrada + "','DD/MM/YYYY') , TO_DATE('" + fecha_salida + "','DD/MM/YYYY'), '" + tipoHabitacion + "',0,0)"
    query_agregar_tupla_RegistroHotel = "INSERT INTO RegistroHotel VALUES ('" + id_reserva + "','" + dni + "')"

    try:
        cursor.execute(query_agregar_tupla_clientes) #Intentamos meter a un cliente (podría darse el caso de que fuese un cliente repetido de otra ocasión)
    except Exception as e:
        print("Cliente ya registrado en el sistema")

    try:
        cursor.execute(query_agregar_tupla_reserva)
        cursor.execute(query_agregar_tupla_RegistroHotel)

    except Exception as e:
        print('ERROR al agregar la tupla clientes o la tupla reserva, no se ha podido crear la reserva, inténtelo de nuevo": ', e)
        return

    print("Reserva realizada con éxito, la información de la reserva creada es la siguiente:\n")
    print(  '\n Codigo de Reserva: ' + str(id_reserva) + ' \
            \n DNI/Pasaporte del Cliente: ' + dni + ' \
            \n Número de teléfono del Cliente: ' + telefono + ' \
            \n Tipo de Habitación Pedida: ' + tipoHabitacion + ' \
            \n Cuenta bancaria del Cliente: ' + cuentaBancaria + ' \
            \n Fecha de Entrada: ' + fecha_entrada + ' \
            \n Fecha de Salida: ' + fecha_salida + '\
            ')

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        cursor.execute("ROLLBACK TO SAVEPOINT DatosRegistrarReserva")
        print("\nReserva de Habitación deshecha. Se debe realizar de nuevo la reserva")
    else:
        print("\nReserva de habitación finalizada")
        connection.commit()

    

#########################################################################
# Función para cuando el cliente realice el check-in en el hotel

def realizarCheckIn(cursor, connection):
    #Pedimos el dni al cliente

    cursor.execute("SAVEPOINT DatosCheckIn")

    cod_reserva = input('Introduzca el código de reserva: ')

    query_buscar_reserva = "SELECT DNI_Pasaporte FROM RegistroHotel WHERE CReserva = '"+cod_reserva+"'"

    cursor.execute(query_buscar_reserva)

    DNI_Pasaporte = cursor.fetchone()
    if (not DNI_Pasaporte):
        print("No se ha detectado ninguna reserva en el sistema con este código, inténtelo de nuevo")
        return
    else:
        print("Se ha detectado una reserva asociado al cliente con ID: ")
        print(DNI_Pasaporte[0])

    #Comprobemos que la fecha de entrada es posterior a la fecha actual y que la fecha de salida es posterior también a la fecha actual, además de comprobar que no se ha realizado ya el check-in de esta reserva

    query_obtener_fechas = "SELECT FechaEntrada,FechaSalida FROM  ReservaHotel WHERE CReserva= '"+cod_reserva+"'"

    cursor.execute(query_obtener_fechas)

    for row in cursor:
        fecha_entrada=row[0]
        fecha_salida=row[1]
    fecha_actual = datetime.today()
    
    if(fecha_entrada>fecha_actual):
        print("La fecha actual es posterior a la fecha de entrada, no puede efecturarse la reserva")
        return
    
    if(fecha_salida<fecha_actual):
        print("Ya no puede efectual el check-in, ya ha acabado su reserva")
        return

    #Comprobamos que esta reserva no ha efectuado todavía el check-in (para no darle dos habitaciones)

    query_buscar_checkin = "SELECT * FROM HabReserva WHERE CReserva = '"  + cod_reserva+ "'"

    cursor.execute(query_buscar_checkin)

    checkin_reserva = cursor.fetchall()

    if(checkin_reserva):
        print("Ya se ha realizado el check-in con esta reserva.")
        return
    
    #Una vez comprobado que todo esté correcto procedemos a la asignación de una habitación, asignaremos una habitación que no está en la tabla "HabReserva" y del tipo indicado

    #Obtenemos el tipo de habitación deseada por el cliente en su reserva

    query_tipo_habitacion = "SELECT TipoHabitacionPedida FROM ReservaHotel WHERE CReserva = '" + cod_reserva + "'"

    cursor.execute(query_tipo_habitacion)

    for row in cursor:
        tipo_hab = row[0]
    tipo_hab = tipo_hab.strip() #Quitamos espacios a la palabra

    #Podemos usar la función "Consultar disponibilidad de una habitación" para ver las habitaciones disponibles y asignar una cualquiera.
 
    lista_hab = habitaciones_disponibles(cursor,tipo_hab)

    #Asignamos la primera habitación que encuentre disponible

    for i in lista_hab:
        num_hab = i[0]
        break

    if(not lista_hab):
        print("No quedan habitaciones disponibles del tipo seleccionado, no se ha podido realizar el check-in.")
        return
    
    #Si hay habitaciones libres creamos el check-in

    query_crear_relacion = "INSERT INTO HabReserva VALUES ('" + str(num_hab) + "','" + cod_reserva + "')"

    try:
        cursor.execute(query_crear_relacion) #Intentamos meter a un cliente (podría darse el caso de que fuese un cliente repetido de otra ocasión)
    except Exception as e:
        print("Ya ha realizado el check_out o a cancelado la reserva, no puede realizar el check_in: ", e)
        return
        
    print("CheckIn realizado correctamente, se va a asignar la habitación: ",num_hab)
    
    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        cursor.execute("ROLLBACK TO SAVEPOINT DatosCheckIn")
        print("\nCheckIn deshecho. Se debe realizar de nuevo el checkin")
    else:
        print("\nCheckIn finalizado")
        connection.commit()
    
#########################################################################
# Función para cuando el cliente realice el check-out del hotel

def realizarCheckOut(cursor, connection):

    cursor.execute("SAVEPOINT DatosCheckOut")

    id_reserva = input('Introduce el código de la reserva: ')

    query_realizar_checkout = "DELETE FROM HabReserva WHERE CReserva ='"+id_reserva+"'"
    query_actualizar_reserva = "UPDATE ReservaHotel SET Check_Out='1' WHERE CReserva='" + id_reserva + "'"

    try:
        cursor.execute(query_realizar_checkout)
        cursor.execute(query_actualizar_reserva)
    except Exception as e:
        print('ERROR al realizar el checkout: ', e)
        return
	
    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        cursor.execute("ROLLBACK TO SAVEPOINT DatosCheckOut")
        print("\nCheckOut deshecho. Se debe realizar de nuevo el checkout")
    else:
        print("\nCheckOut finalizado")
        connection.commit()

#########################################################################
# Función para consultar la disponibilidad de un tipo de 
# habitación dado

def consultarDisponibilidad(cursor):

    tipoHabitacion = input('Introduzca el tipo de habitación de la que quiere comprobar la disponibilidad (individual, doble o suite).\n Si no introduce ninguno de estos tipos se mostrará la disponibilidad de todas las habitaciones del hotel: ')
    
    lista_habitaciones = habitaciones_disponibles(cursor,tipoHabitacion)

    print("Lista de habitaciones del tipo " + tipoHabitacion + " no ocupadas: ")

    for s in lista_habitaciones:
        print(s[0])
   
#########################################################################
# Función para cancelar una reserva del hotel

def cancelarReserva(cursor, connection):

    cursor.execute("SAVEPOINT DatosCancelarReserva")

    id_reserva = input('Introduce el código de la reserva: ')

    query_cancelar_reserva = "UPDATE ReservaHotel SET Cancelada=1 WHERE CReserva = '" + id_reserva + "'"

    try:
        cursor.execute(query_cancelar_reserva)
    except Exception as e:
        print('ERROR al cancelar la reserva": ', e)
        return


    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        cursor.execute("ROLLBACK TO SAVEPOINT DatosCancelarReserva")
        print("\nReserva no cancelada. Se debe realizar de nuevo la cancelación")
    else:
        print("\nCancelación finalizada")
        connection.commit()


#########################################################################
# Menú con las diferentes opciones del subsistema Reservas del Hotel

def menuReservasHotel(cursor, connection):
    terminar = False

    while(not terminar):
        print("\n2.1) Registrar una nueva reserva")
        print("2.2) Realizar check-in")
        print("2.3) Realizar check-out")
        print("2.4) Consultar disponibilidad de un tipo de habitación")
        print("2.5) Cancelar una reserva")
        print("2.6) Volver al menú principal")
    
        option = pedirOpcion(6)

        match option:
            case 1:
                registrarReserva(cursor, connection)
            case 2:
                realizarCheckIn(cursor, connection)
            case 3:
                realizarCheckOut(cursor, connection)
            case 4:
                consultarDisponibilidad(cursor)
            case 5:
                cancelarReserva(cursor, connection)
            case 6:
                terminar=True