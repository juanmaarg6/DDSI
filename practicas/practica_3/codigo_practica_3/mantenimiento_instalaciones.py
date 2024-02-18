# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Subsistema: Mantenimiento de Instalaciones (realizado por Jesús García León)

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
# Función para añadir un desperfecto

def añadirDesperfecto(cursor,connection):
    terminar = False
    while(not terminar):
        cd = input("Introduzca el código del desperfecto: ")
        prio = input("Introduzca la prioridad: ")
        descripcion = input("Introduzca una descripción: ")
        fecha = input("Introduzca la fecha: ")
        hab = input("Introduzca la habitación: ")

        print(f"Se añadirá el desperfecto con: \n Código: {cd} \
                \n Prioridad: {prio} \
                \n Descripción: {descripcion} \
                \n Fecha: {fecha} \
                \n Habitación: {hab}")

        query_insertar_desperfecto = "INSERT INTO Desperfecto VALUES (:cd, :prio, :descripcion, TO_DATE(:fecha, 'DD/MM/YYYY'))"
        query_insertar_reparacion = "INSERT INTO Reparacion VALUES (:cd, :hab, NULL)"

        cursor.execute("SAVEPOINT NuevoDesperfecto")
        try:
            cursor.execute(query_insertar_desperfecto, [cd, prio, descripcion,fecha])
            cursor.execute(query_insertar_reparacion, [cd, hab])
        except Exception as e:
            print("Error al añadir un nuevo desperfecto", e)
            cursor.execute("ROLLBACK TO NuevoDesperfecto")

        aniadir = ''

        while(aniadir != 'S' and aniadir != 'N'):
            aniadir = input("¿Desea añadir otro desperfecto? [S/N]: ")

        if(aniadir == 'N'):
            terminar = True

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        connection.rollback()
    
    connection.commit()

#########################################################################
# Función para cambiar el presupuesto de una reparacion

def asignarPresupuesto(cursor, connection):
    cd = input("Introduzca el código del desperfecto: ")
    hab = input("Introduzca la habitación: ")
    presupuesto = input("Introduzca el presupuesto: ")

    query_borrar_presupuesto = "DELETE FROM Reparacion \
                                  WHERE CDesperfecto = :cd AND NumeroHabitacion = :hab"
    
    query_insertar_presupuesto = "INSERT INTO REPARACION VALUES(:cd, :hab, :presupuesto)"

    print(f"Se actualizará el presupuesto de: \n \
           Código: {cd} \n \
           Habitación: {hab} \n \
           Presupuesto: {presupuesto}")

    try:
        cursor.execute(query_borrar_presupuesto, [cd, hab])
    except Exception as e:
        connection.rollback()
        print("Error al añadir un nuevo presupuesto", e)
    try:
        cursor.execute(query_insertar_presupuesto, [cd, hab, presupuesto])
    except Exception as e:
        print("Error al añadir un nuevo presupuesto", e)
        connection.rollback()

    connection.commit()

#########################################################################
# Función para consultar el precio de reparacion

def consultarPrecioReparacionDesperfecto(cursor):
    CDesperfecto = input("Introduzca el codigo del desperfecto: ")
    NumHab = int(input("Introduzca el numero de habitación: "))

    query_peticion = "SELECT PrecioReparacion from Reparacion\
                      WHERE CDesperfecto = :CDesperfecto \
                      AND NumeroHabitacion = :NumHab"

    try:
        cursor.execute(query_peticion,[CDesperfecto, NumHab])
        Precio = cursor.fetchall()
        print(f"El precio de reparacion del desperfecto {CDesperfecto} es: {Precio[0][0]}")
    except Exception as e:
        print("ERROR al mostrar el precio de reparación", e)

#########################################################################
# Función para consultar desperfectos

def consultarDesperfectos(cursor):
    try:
        cursor.execute('SELECT * FROM Desperfecto ORDER BY Prioridad ASC')
        desperfecto = cursor.fetchall()

        print('\nTABLA "Desperfecto": ')

        tuplas_desperfecto = [] # Lista donde cada elemento suyo será una tupla de la tabla "Desperfecto" puesta en forma de lista
                                # (Por tanto, tenemos una lista de listas)
        for d in desperfecto:
            tuplas_desperfecto.append([ d[0], d[1] , d[2], d[3].strftime('%d/%m/%Y') ])
        
        print(tabulate(tuplas_desperfecto, headers=["CDesperfecto", "Prioridad", "Descripcion", "FechaObservacion"], tablefmt='fancy_grid'))

    except Exception as e:
        print('ERROR al MOSTRAR la tabla "Desperfecto": ', e)

#########################################################################
# Función para consultar el stock de limpieza

def consultarStockLimpieza(cursor):
    try:
        cursor.execute('SELECT CUtensilio, Nombre, Stock FROM Utensilio')
        utensilio = cursor.fetchall()

        print('\n"Utensilios": ')

        tuplas_utensilio = [] # Lista donde cada elemento suyo será una tupla de la tabla "Utensilio" puesta en forma de lista
                              # (Por tanto, tenemos una lista de listas)
        for u in utensilio:
            tuplas_utensilio.append([ u[0], u[1], u[2] ])
        
        print(tabulate(tuplas_utensilio, headers=["CUtensilio", "Nombre", "Stock"], tablefmt='fancy_grid'))

    except Exception as e:
        print('ERROR al MOSTRAR los Utensilios: ', e)

#########################################################################
# Menú con las diferentes opciones del subsistema Mantenimiento de 
# Instalaciones

def menuMantenimiento(cursor, connection):
    terminar = False

    while(not terminar):
        print("\n5.1) Añadir un desperfecto")
        print("5.2) Asignar presupuesto a un desperfecto existente")
        print("5.3) Consultar el precio de la reparacion de un desperfecto")
        print("5.4) Consultar desperfecto en orden de prioridad")
        print("5.5) Consultar Stock de productos de limpieza")
        print("5.6) Volver al menú principal")

        option = pedirOpcion(6)

        match option:
            case 1:
                añadirDesperfecto(cursor, connection)
            case 2:
                asignarPresupuesto(cursor, connection)
            case 3:
                consultarPrecioReparacionDesperfecto(cursor)
            case 4:
                consultarDesperfectos(cursor)
            case 5:
                consultarStockLimpieza(cursor)
            case 6:
                terminar = True