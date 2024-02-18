-- PARA EJECUTAR ESTE ARCHIVO EN SQL DEVELOPER, DEBEMOS EJECUTAR LA SIGUIENTE LÍNEA:
-- @path\tablas.sql;

---------------------------------------------------------------
------------------------ BORRAR TABLAS ------------------------
---------------------------------------------------------------

DROP TABLE Utensilio;
DROP TABLE Reparacion;
DROP TABLE Desperfecto;
DROP TABLE HabReserva;
DROP TABLE Habitacion;
DROP TABLE RegistroHotel;
DROP TABLE ReservaHotel;
DROP TABLE ReservaParking;
DROP TABLE PlazaParking;
DROP TABLE OpinionAct;
DROP TABLE ReservaAct;
DROP TABLE Cliente;
DROP TABLE OrganizacionAct;
DROP TABLE ActividadOcio;
DROP TABLE Trabajador;

---------------------------------------------------------------
--------------- CREAR TABLAS E INSERTAR TUPLAS ----------------
---------------------------------------------------------------

----- Tabla Trabajador -----

CREATE TABLE Trabajador (
    DNI_Pasaporte VARCHAR2(15) PRIMARY KEY,
    Nombre VARCHAR2(20) NOT NULL,
    Apellidos VARCHAR2(30) NOT NULL,
    Cargo VARCHAR2(20),
    Departamento VARCHAR2(20),
    FechaNacimiento DATE,
    Telefono VARCHAR2(15) NOT NULL,
    CorreoElectronico VARCHAR2(50) UNIQUE
);


INSERT INTO Trabajador VALUES ('79212958G', 'Antonio', 'Morales Reinos', 'Recepcionista', 'Recepcion', TO_DATE('24/11/1984','dd/mm/yyyy'), '630847299', 'antoniomr@gmail.com');
INSERT INTO Trabajador VALUES ('18371847A', 'Andrea', 'Gutierrez Alfaro', 'Directora', 'Direccion', TO_DATE('08/01/2001','dd/mm/yyyy') , '638492483', 'andreagalf@gmail.com');
INSERT INTO Trabajador VALUES ('18371856B', 'Benito', 'Perez Garcia', 'Camarero', 'Restauracion', TO_DATE('10/11/1999','dd/mm/yyyy'), '628393849', 'benitopg@gmail.com');
INSERT INTO Trabajador VALUES ('18371833C', 'Sara', 'Sanchez Torres', 'Cocinera', 'Restauracion', TO_DATE('18/11/1978','dd/mm/yyyy'), '628474839', 'sarast@gmail.com');
INSERT INTO Trabajador VALUES ('18371822D', 'Ana', 'Nuñez Quesada', 'Limpiadora', 'Limpieza', TO_DATE('21/11/1988','dd/mm/yyyy'), '684235252', 'ananq@gmail.com');

----- Tabla ActividadOcio -----

CREATE TABLE ActividadOcio (
    ActOcio VARCHAR2(10) PRIMARY KEY,
    Nombre VARCHAR2(20) NOT NULL,
    Descripcion VARCHAR2(100),
    Fecha DATE,
    Hora DATE,
    NumPlazas NUMBER(2,0) CHECK(NumPlazas >= 0)
);

INSERT INTO ActividadOcio VALUES ('#A00000001', 'Fiesta Ibicenca', 'Fiesta donde todo el mundo va vestido de blanco', TO_DATE('01/12/2022','DD/MM/YYYY'), TO_DATE('12:00','HH24:MI'), 40);
INSERT INTO ActividadOcio VALUES ('#A00000002', 'Aquagym', 'Variante del aerobic que se realiza en la piscina', TO_DATE('02/11/2022','DD/MM/YYYY'), TO_DATE('18:00','HH24:MI'), 18);
INSERT INTO ActividadOcio VALUES ('#A00000003', 'Gymkana', 'Diferentes juegos de competicion en equipo', TO_DATE('14/10/2022','DD/MM/YYYY'), TO_DATE('11:30','HH24:MI'), 30);
INSERT INTO ActividadOcio VALUES ('#A00000004', 'Yoga', 'Conjunta de tecnicas de concentracion para conseguir un mayor control fisico y mental', TO_DATE('16/12/2022','DD/MM/YYYY'), TO_DATE('12:45','HH24:MI'), 10);
INSERT INTO ActividadOcio VALUES ('#A00000005', 'Concurso de Cocina', 'Evento para poner a prueba las habilidades culinarias', TO_DATE('01/02/2023','DD/MM/YYYY'), TO_DATE('13:00','HH24:MI'), 14);

----- Tabla OrganizacionAct -----

CREATE TABLE OrganizacionAct (
    ActOcio VARCHAR2(10) REFERENCES ActividadOcio(ActOcio) PRIMARY KEY,
    DNI_Pasaporte VARCHAR2(15) REFERENCES Trabajador(DNI_Pasaporte)
);

INSERT INTO OrganizacionAct VALUES ('#A00000001', '18371847A');
INSERT INTO OrganizacionAct VALUES ('#A00000002', '79212958G');
INSERT INTO OrganizacionAct VALUES ('#A00000003', '18371847A');
INSERT INTO OrganizacionAct VALUES ('#A00000004', '79212958G');
INSERT INTO OrganizacionAct VALUES ('#A00000005', '18371833C');

----- Tabla Cliente -----

CREATE TABLE Cliente (
    DNI_Pasaporte VARCHAR2(15) PRIMARY KEY,
    Telefono VARCHAR2(15) NOT NULL,
    CuentaBancaria VARCHAR2(30)
);

INSERT INTO Cliente VALUES ('77654234H', '603345683', 'ISPB12341223456');
INSERT INTO Cliente VALUES ('77614234S', '603345681', 'ISPB12341231111');
INSERT INTO Cliente VALUES ('77623434L', '678094345', 'ISPB12341232233');
INSERT INTO Cliente VALUES ('77611224A', '603345681', 'ISPB12123234123');
INSERT INTO Cliente VALUES ('77645678D', '612367894', 'ISPB12112345123');

----- Tabla ReservaAct -----

CREATE TABLE ReservaAct (
	DNI_Pasaporte VARCHAR2(15) REFERENCES Cliente(DNI_Pasaporte),
	ActOcio VARCHAR2(10) REFERENCES ActividadOcio(ActOcio),
	FechaReserva DATE,
	HoraReserva DATE,
	NumPlazas INT CHECK(NumPlazas > 0),

	PRIMARY KEY(DNI_Pasaporte, ActOcio)
);

INSERT INTO ReservaAct VALUES ('77623434L', '#A00000001', TO_DATE('01/12/2022','DD/MM/YYYY'), TO_DATE('12:00','HH24:MI'), 4);
INSERT INTO ReservaAct VALUES ('77611224A', '#A00000002', TO_DATE('02/11/2022','DD/MM/YYYY'), TO_DATE('18:00','HH24:MI'), 2);
INSERT INTO ReservaAct VALUES ('77623434L', '#A00000005', TO_DATE('01/02/2023','DD/MM/YYYY'), TO_DATE('13:00','HH24:MI'), 1);

----- Tabla OpinionAct -----

CREATE TABLE OpinionAct (
	DNI_Pasaporte VARCHAR2(15) REFERENCES Cliente(DNI_Pasaporte),
	ActOcio VARCHAR2(10) REFERENCES ActividadOcio(ActOcio),
	Opinion VARCHAR2(200),
	Puntuacion INT CHECK(Puntuacion >= 0 AND Puntuacion <= 10) NOT NULL
);

INSERT INTO OpinionAct VALUES ('77623434L', '#A00000001', 'Perfecto', 10);
INSERT INTO OpinionAct VALUES ('77611224A', '#A00000002', 'Mejorable', 4);

----- Tabla PlazaParking -----

CREATE TABLE PlazaParking (
	NumeroPlaza NUMBER(3,0) PRIMARY KEY CHECK(NumeroPlaza >= 0) NOT NULL
);

INSERT INTO PlazaParking VALUES ('17');
INSERT INTO PlazaParking VALUES ('253');
INSERT INTO PlazaParking VALUES ('467');
INSERT INTO PlazaParking VALUES ('682');
INSERT INTO PlazaParking VALUES ('947');

----- Tabla ReservaParking -----

CREATE TABLE ReservaParking (
	NumeroPlaza INT PRIMARY KEY REFERENCES PlazaParking(NumeroPlaza),
	DNI_Pasaporte VARCHAR2(15) REFERENCES Cliente(DNI_Pasaporte) UNIQUE,
    TiempoOcupacion INT 
);

INSERT INTO ReservaParking VALUES ('947', '77623434L', 98);

----- Tabla ReservaHotel -----

CREATE TABLE ReservaHotel (
    CReserva VARCHAR2(10) PRIMARY KEY,
    FechaEntrada DATE NOT NULL,
    FechaSalida DATE NOT NULL,
    TipoHabitacionPedida VARCHAR2(10) NOT NULL,    
    Check_out NUMBER(1,0) CHECK(Check_out = 0 OR Check_out = 1),
    Cancelada NUMBER(1,0) CHECK(Cancelada = 0 OR Cancelada = 1)
);

INSERT INTO ReservaHotel VALUES ('#R00000001', TO_DATE('01/11/2022','dd/mm/yyyy'), TO_DATE('10/12/2022','dd/mm/yyyy'), 'Suite', 1, 0);
INSERT INTO ReservaHotel VALUES ('#R00000002', TO_DATE('30/11/2022','dd/mm/yyyy'), TO_DATE('04/12/2022','dd/mm/yyyy'), 'Doble', 1, 0);
INSERT INTO ReservaHotel VALUES ('#R00000003', TO_DATE('12/01/2023','dd/mm/yyyy'), TO_DATE('02/02/2023','dd/mm/yyyy'), 'Individual', 0, 0);
INSERT INTO ReservaHotel VALUES ('#R00000004', TO_DATE('13/01/2023','dd/mm/yyyy'), TO_DATE('26/01/2023','dd/mm/yyyy'), 'Suite', 0, 0);
INSERT INTO ReservaHotel VALUES ('#R00000005', TO_DATE('02/01/2023','dd/mm/yyyy'), TO_DATE('05/01/2023','dd/mm/yyyy'), 'Doble', 0, 1);

----- Tabla RegistroHotel -----

CREATE TABLE RegistroHotel (
    CReserva VARCHAR2(10) REFERENCES ReservaHotel(CReserva) PRIMARY KEY,
    DNI_Pasaporte VARCHAR2(15) REFERENCES Cliente(DNI_Pasaporte)
);

INSERT INTO RegistroHotel VALUES ('#R00000001', '77614234S');
INSERT INTO RegistroHotel VALUES ('#R00000002', '77654234H');
INSERT INTO RegistroHotel VALUES ('#R00000003', '77623434L');
INSERT INTO RegistroHotel VALUES ('#R00000004', '77611224A');
INSERT INTO RegistroHotel VALUES ('#R00000005', '77645678D');

----- Tabla Habitacion -----

CREATE TABLE Habitacion (
    NumeroHabitacion NUMBER(3,0) PRIMARY KEY CHECK(NumeroHabitacion > 0),
    TipoHabitacion VARCHAR2(10) NOT NULL
);

INSERT INTO Habitacion VALUES (8, 'Individual');
INSERT INTO Habitacion VALUES (123, 'Doble');
INSERT INTO Habitacion VALUES (369, 'Suite');
INSERT INTO Habitacion VALUES (401, 'Individual');
INSERT INTO Habitacion VALUES (500, 'Doble');
INSERT INTO Habitacion VALUES (673, 'Doble');
INSERT INTO Habitacion VALUES (837, 'Individual');

----- Tabla HabReserva -----

CREATE TABLE HabReserva (
    NumeroHabitacion INT REFERENCES Habitacion(NumeroHabitacion) PRIMARY KEY,
    CReserva VARCHAR2(10) REFERENCES ReservaHotel(CReserva) UNIQUE
);

INSERT INTO HabReserva VALUES (369, '#R00000004');
INSERT INTO HabReserva VALUES (401, '#R00000003');

----- Tabla Desperfecto -----

CREATE TABLE Desperfecto (
    CDesperfecto VARCHAR2(10) PRIMARY KEY,
    Prioridad NUMBER(3,0) CHECK(Prioridad >= 0),
    Descripcion VARCHAR2(200) NOT NULL,
    FechaObservacion DATE
);

INSERT INTO Desperfecto VALUES ('#D00000001', NULL, 'Mancha de humedad en la habitacion 673', TO_DATE('29/11/2022','dd/mm/yyyy'));
INSERT INTO Desperfecto VALUES ('#D00000002', 2, 'No hay luz en la habitacion 837', TO_DATE('30/11/2022','dd/mm/yyyy'));
INSERT INTO Desperfecto VALUES ('#D00000003', 1, 'No funciona la cadena del vater en la habitacion 123', TO_DATE('05/01/2023','dd/mm/yyyy'));

----- Tabla Reparacion -----

CREATE TABLE Reparacion (
    CDesperfecto VARCHAR2(10) REFERENCES Desperfecto(CDesperfecto) PRIMARY KEY,
    NumeroHabitacion INT REFERENCES Habitacion(NumeroHabitacion),
    PrecioReparacion NUMBER(8,2) CHECK(PrecioReparacion > 0)
);

INSERT INTO Reparacion VALUES ('#D00000003', 123, 56.50);
INSERT INTO Reparacion VALUES ('#D00000002', 837, NULL);

----- Tabla Utensilio -----

CREATE TABLE Utensilio (
    CUtensilio VARCHAR2(10) PRIMARY KEY,
    Nombre VARCHAR2(20) UNIQUE,
    Stock INT CHECK(Stock > 0),
    CompaniaDistrib VARCHAR2(20)
);

INSERT INTO Utensilio VALUES ('#U00000001', 'Tornillo Plano', 500, 'Screws Company');
INSERT INTO Utensilio VALUES ('#U00000002', 'Tornillo Hexagonal', 329, 'Screws Company');
INSERT INTO Utensilio VALUES ('#U00000003', 'Tornillo Redondo', 446, 'Screws Company');
INSERT INTO Utensilio VALUES ('#U00000004', 'Bombilla', 97, 'Lamps Company');
INSERT INTO Utensilio VALUES ('#U00000005', 'Tirador Vater', 49, 'WC Products');
INSERT INTO Utensilio VALUES ('#U00000006', 'Bote Limpiacristales', 15, 'Cleaning S.A.');
