# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Subsistema: Trabajadores (realizado por Mónica Calzado Granados)

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
# Función para dar de alta un trabajador

def añadirTrabajador(cursor,connection):
    terminar = False
    while(not terminar):
        dni = input("\nIntroduzca el DNI/Pasaporte del trabajador: ")
        nombre = input("Introduzca el nombre: ")
        apellidos = input("Introduzca los apellidos: ")
        cargo = input("Introduzca el cargo: ")
        departamento = input("Introduzca el departamento: ")
        fecha_n = input("Introduzca la fecha de nacimiento: ")
        telefono = input("Introduzca el teléfono móvil: ")
        correo = input("Introduzca el correo electrónico: ")

        print(f"Se dará de alta al trabajador con: \
                \n DNI/Pasaporte: {dni} \
                \n Nombre: {nombre} \
                \n Apellidos: {apellidos} \
                \n Cargo: {cargo} \
                \n Departamento: {departamento} \
                \n Fecha de nacimiento: {fecha_n} \
                \n Teléfono móvil: {telefono} \
                \n Correo electrónico: {correo}")

        query_insertar_trabajador = "INSERT INTO Trabajador VALUES (:dni, :nombre, :apellidos, :cargo, :departamento, TO_DATE(:fecha_n, 'DD/MM/YYYY'), :telefono, :correo)"

        cursor.execute("SAVEPOINT NuevoTrabajador")
        try:
            cursor.execute(query_insertar_trabajador, [dni, nombre, apellidos, cargo, departamento, fecha_n, telefono, correo])
        except Exception as e:
            print("Error al dar de alta un nuevo trabajador", e)
            cursor.execute("ROLLBACK TO NuevoTrabajador")

        aniadir = ''

        while(aniadir != 'S' and aniadir != 'N'):
            aniadir = input("¿Desea añadir otro trabajador? [S/N]: ")

        if(aniadir == 'N'):
            terminar = True

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        connection.rollback()
    
    connection.commit()

#########################################################################
# Función para dar de baja a un trabajador

def eliminarTrabajador(cursor,connection):
    terminar = False
    while(not terminar):
        dni = input("Introduzca el DNI/Pasaporte del trabajador: ")

        print(f"Se dará de baja al trabajador con: \
                \n DNI/Pasaporte: {dni}")

        query_eliminar_trabajador = "DELETE FROM Trabajador WHERE DNI_Pasaporte = '"+dni+"' "
        
        cursor.execute("SAVEPOINT EliminarTrabajador")
        try:
            cursor.execute(query_eliminar_trabajador)
        except Exception as e:
            print("Error al dar de baja al trabajador", e)
            cursor.execute("ROLLBACK TO EliminarTrabajador")

        aniadir = ''

        while(aniadir != 'S' and aniadir != 'N'):
            aniadir = input("¿Desea dar de baja a otro trabajador? [S/N]: ")

        if(aniadir == 'N'):
            terminar = True

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        connection.rollback()
    
    connection.commit()


#########################################################################
# Función para mostrar los trabajadores de un departamento

def mostrarTrabajadores(cursor):
    departamento = input("Introduzca un departamento: ")

    print(f"Se mostrarán los trabajadores pertenecientes al departamento: {departamento}")

    query_mostrar_trabajadores = "SELECT * FROM Trabajador WHERE Departamento = '"+departamento+"' "

    try:
        cursor.execute(query_mostrar_trabajadores)
        trabajador = cursor.fetchall()
        tuplas_trabajador = []

        for t in trabajador:
            tuplas_trabajador.append([ t[0], t[1] , t[2] ])

        print(tabulate(tuplas_trabajador, headers=["Nombre", "Apellidos", "Cargo"], tablefmt='fancy_grid'))
    except Exception as e:
        print("Error al mostrar los trabajadores", e)

#########################################################################
# Función para modificar datos de un trabajador

def modificarTrabajador(cursor,connection):
    terminar = False
    while(not terminar):
        dni = input("Introduzca el DNI/Pasaporte del trabajador: ")

        #Primero tenemos que comprobar si dicho trabajador existe
        query_consultar_trabajador = "SELECT * FROM Trabajador WHERE DNI_Pasaporte = '"+dni+"' "
        cursor.execute(query_consultar_trabajador)
        trabajador = cursor.fetchone()
        if trabajador:
            print(f"Se modificará al trabajador con DNI/Pasaporte: {dni}" )
        else:
            print(f"El trabajador no existe")
            return

        
        print("\n\n Elige qué atributo quieres modificar:")
        print("\n1) Nombre")
        print("2) Apellidos")
        print("3) Cargo")
        print("4) Departamento")
        print("5) Fecha de nacimiento")
        print("6) Teléfono móvil")
        print("7) Correo electrónico")

        num = 0
        while(num <= 0 or num > 7):
            try:
                num = int(input("\nIntroduzca una opcion (Número entero entre 1 y 7): "))
            except ValueError as v:
                print('ERROR al procesar la OPCIÓN INTRODUCIDA: ', v)
     
        match num:
            case 1:
                nombre = input("Introduzca el nuevo nombre: ")
                query_modificar_trabajador = "UPDATE Trabajador SET Nombre='"+nombre+"' WHERE DNI_Pasaporte='"+dni+"' " 
            case 2:
                apellidos = input("Introduzca los nuevos apellidos: ")
                query_modificar_trabajador = "UPDATE Trabajador SET Apellidos='"+apellidos+"' WHERE DNI_Pasaporte='"+dni+"' " 
            case 3:
                cargo = input("Introduzca el nuevo cargo: ")
                query_modificar_trabajador = "UPDATE Trabajador SET Cargo='"+cargo+"' WHERE DNI_Pasaporte='"+dni+"' " 
            case 4:
                departamento = input("Introduzca el nuevo departamento: ")
                query_modificar_trabajador = "UPDATE Trabajador SET Departamento='"+departamento+"' WHERE DNI_Pasaporte='"+dni+"' " 
            case 5:
                fecha_n = input("Introduzca la nueva fecha de nacimiento: ")
                query_modificar_trabajador = "UPDATE Trabajador SET FechaNacimiento=TO_DATE('"+fecha_n+"', 'DD/MM/YYYY') WHERE DNI_Pasaporte='"+dni+"' " 
            case 6:
                telefono = input("Introduzca el nuevo teléfono móvil: ")
                query_modificar_trabajador = "UPDATE Trabajador SET Telefono='"+telefono+"' WHERE DNI_Pasaporte='"+dni+"' " 
            case 7:
                correo = input("Introduzca el nuevo correo electrónico: ")
                query_modificar_trabajador = "UPDATE Trabajador SET CorreoElectronico='"+correo+"' WHERE DNI_Pasaporte='"+dni+"' " 
            

        cursor.execute("SAVEPOINT TrabajadorModificado")
        try:
            cursor.execute(query_modificar_trabajador)
        except Exception as e:
            print("Error al modificar al trabajador", e)
            cursor.execute("ROLLBACK TO TrabajadorModificado")

        aniadir = ''

        while(aniadir != 'S' and aniadir != 'N'):
            aniadir = input("¿Desea modificar los datos de otro trabajador? [S/N]: ")

        if(aniadir == 'N'):
            terminar = True

    guardar_cambios = ''

    while(guardar_cambios != 'S' and guardar_cambios != 'N'):
        guardar_cambios = input("¿Desea guardar los cambios? [S/N]: ")

    if(guardar_cambios == 'N'):
        connection.rollback()
    
    connection.commit()


#########################################################################
# Función para consultar los datos de un trabajador

def consultarTrabajador(cursor):
    terminar = False
    while(not terminar):
        dni = input("Introduzca el DNI/Pasaporte del trabajador: ")

        query_consultar_trabajador = "SELECT * FROM Trabajador WHERE DNI_Pasaporte = '"+dni+"' "

       
        try:
            cursor.execute(query_consultar_trabajador)
            trabajador = cursor.fetchall()
            tuplas_trabajador = []

            for t in trabajador:
                tuplas_trabajador.append([  t[0], t[1] , t[2], t[3], t[4], t[5].strftime('%d/%m/%Y'), t[6], t[7]  ])

            print(tabulate(trabajador, headers=["DNI_Pasaporte", "Nombre", "Apellidos", "Cargo", "Departamento", "FechaNacimiento", "Telefono", "CorreoElectronico"], tablefmt='fancy_grid'))
        except Exception as e:
            print("Error al consultar el trabajador", e)
        
        aniadir = ''

        while(aniadir != 'S' and aniadir != 'N'):
            aniadir = input("¿Desea consultar los datos de otro trabajador? [S/N]: ")

        if(aniadir == 'N'):
            terminar = True

#########################################################################
# Menú con las diferentes opciones del subsistema Trabajadores

def menuTrabajadores(cursor, connection):
    terminar = False

    while(not terminar):
        print("\n1.1) Dar de alta a un nuevo trabajador")
        print("1.2) Dar de baja a un trabajador")
        print("1.3) Mostrar trabajadores de un departamento")
        print("1.4) Modificar los datos de un trabajador")
        print("1.5) Consultar datos de un trabajador")
        print("1.6) Volver al menú principal")

        option = pedirOpcion(6)

        match option:
            case 1:
                añadirTrabajador(cursor,connection)
            case 2:
                eliminarTrabajador(cursor, connection)
            case 3:
                mostrarTrabajadores(cursor)
            case 4:
                modificarTrabajador(cursor, connection)
            case 5:
                consultarTrabajador(cursor)
            case 6:
                terminar = True