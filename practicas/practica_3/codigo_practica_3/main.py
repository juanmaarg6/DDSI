# Práctica 3 DDSI
# Grupo: DGIIM Hotels International
# Programa Principal

import oracledb         # py -m pip install oracledb   (para aquellas acciones relacionadas con la base de datos)

import trabajadores as tr
import reservas_hotel as rh
import actividades_ocio as act
import parking as pk
import mantenimiento_instalaciones as mnt

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
# Función para establecer la conexión con la base de datos

def connect():
    server = '1521:oracle0.ugr.es/practbd.oracle0.ugr.es'
    user = 'x9559494'
    password = 'x9559494'

    try:
        connection = oracledb.connect(user=user,password=password,dsn=server)
        print('\nCONEXIÓN A LA BASE DE DATOS REALIZADA CON ÉXITO')
        return connection
    except Exception as e:
        print ('\nERROR al CONECTARSE a la BASE DE DATOS: ', e)
        exit()

#########################################################################
# Función para cerrar la conexión con la base de datos

def disconnect(cursor, connection):
    cursor.close()
    connection.close()
    print('\nCONEXIÓN A LA BASE DE DATOS CERRADA CON ÉXITO\n')

#########################################################################
# Función principal del programa

def main():
    connection = connect()
    cursor = connection.cursor()

    terminar = False

    while(not terminar):
        print("\n1) Trabajadores")
        print("2) Reservas del Hotel")
        print("3) Actividades de Ocio")
        print("4) Parking")
        print("5) Mantenimiento de Instalaciones")
        print("6) Salir del programa y cerrar conexión a BD")

        option = pedirOpcion(6)

        match option: 
            case 1:
                tr.menuTrabajadores(cursor, connection)
            case 2:
                rh.menuReservasHotel(cursor, connection)
            case 3:
                act.menuActividadesOcio(cursor, connection)
            case 4:
                pk.menuParking(cursor, connection)
            case 5:
                mnt.menuMantenimiento(cursor, connection)
            case 6:
                disconnect(cursor, connection)
                terminar = True

if __name__ == "__main__":
    main()