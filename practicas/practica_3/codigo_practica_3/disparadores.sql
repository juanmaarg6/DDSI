---------------------------------------------------------------
--------------------- BORRAR DISPARADORES ---------------------
---------------------------------------------------------------

DROP TRIGGER edad_min_laboral;
DROP TRIGGER borrado_cascada_tr_act1;
DROP TRIGGER borrado_cascada_tr_act2;
DROP TRIGGER tr_no_aceptar_reservas;
DROP TRIGGER tr_comprobacion_cancelacion;
DROP TRIGGER tr_comprobar_fechas;
DROP TRIGGER opinion_dni_cliente;
DROP TRIGGER no_reserva_act_ocio;
DROP TRIGGER no_reserva_parking;
DROP TRIGGER precio_rep_no_modif;
DROP TRIGGER no_superar_presupuesto;

---------------------------------------------------------------
--------------------- CREAR DISPARADORES ----------------------
---------------------------------------------------------------

-- Realizados por Mónica Calzado Granados (Responsable del subsistema "Trabajadores")

CREATE OR REPLACE TRIGGER edad_min_laboral
  BEFORE INSERT OR UPDATE ON Trabajador
  FOR EACH ROW
BEGIN 
  IF (trunc(months_between(to_date(to_char(SYSDATE, 'dd/mm/yyyy'), 'dd/mm/yyyy'), to_date(to_char(:new.FechaNacimiento, 'dd/mm/yyyy'), 'dd/mm/yyyy'))/12) < 16) THEN
    RAISE_APPLICATION_ERROR(-20001, 'El trabajador debe ser mayor de 16 años');
  END IF;
END;
  

CREATE OR REPLACE TRIGGER borrado_cascada_tr_act1
  BEFORE DELETE ON Trabajador
  FOR EACH ROW
BEGIN
    --Borramos OrganizacionAct antes que la Actividad de ocio pues la primera referencia a la segunda
    DELETE FROM OrganizacionAct WHERE DNI_Pasaporte= :OLD.DNI_Pasaporte;
END;


CREATE OR REPLACE TRIGGER borrado_cascada_tr_act2
  AFTER DELETE ON OrganizacionAct
  FOR EACH ROW
BEGIN
    --Este trigger se ejecuta como consecuencia de borrado_cascada_tr_act1 
    --Tras borrar OrganizacionAct eliminamos las otras dos referencias al campo ActOcio de ActividadOcio
    --y por último borramos la Actividad de ocio
    DELETE FROM ReservaAct WHERE ActOcio = :OLD.ActOcio;
    DELETE FROM OpinionAct WHERE ActOcio = :OLD.ActOcio;
    DELETE FROM ActividadOcio WHERE ActOcio = :OLD.ActOcio;
END;



-- Realizados por Alejandro Cárdenas Barranco (Responsable del subsistema "Reservas del Hotel")

CREATE OR REPLACE TRIGGER tr_no_aceptar_reservas
BEFORE INSERT ON HabReserva
FOR EACH ROW
DECLARE
   c_out NUMBER(1,0);
   cancela NUMBER(1,0);
BEGIN
   SELECT Check_out,cancelada INTO c_out,cancela FROM ReservaHotel WHERE CReserva = :NEW.CReserva;
   IF (c_out = 1 or cancela = 1) THEN
      RAISE_APPLICATION_ERROR(-20001, 'No se puede registrar una habitación para una reserva que ya ha realizado el check-out o se ha cancelado');
   END IF;
END;


CREATE OR REPLACE TRIGGER tr_comprobacion_cancelacion
BEFORE UPDATE ON ReservaHotel
FOR EACH ROW
DECLARE
  l_count       INTEGER;
BEGIN
  -- Comprobar si existen reservas en HabReserva para la reserva en cuestión
  SELECT COUNT(*) INTO l_count FROM HabReserva WHERE CReserva = :new.CReserva;

  -- Comprobar que se está estableciendo Cancelada en true
  IF :new.Cancelada = 1 AND :old.Cancelada = 0 THEN
    -- Comprobar si existen reservas en HabReserva para la reserva en cuestión
    IF l_count > 0 THEN
      RAISE_APPLICATION_ERROR(-20001, 'No se puede cancelar una reserva en la que se haya realizado un check-in');
    END IF;
  END IF;
END;


CREATE OR REPLACE TRIGGER tr_comprobar_fechas
  BEFORE INSERT OR UPDATE ON ReservaHotel
  FOR EACH ROW
BEGIN
  IF :new.FechaSalida <= :new.FechaEntrada THEN
    RAISE_APPLICATION_ERROR(-20001, 'La fecha de salida debe ser posterior a la fecha de entrada');
  END IF;
END;



-- Realizados por Álvaro Rodríguez Gallardo (Responsable del subsistema "Actividades de Ocio")

CREATE OR REPLACE TRIGGER no_reserva_act_ocio
BEFORE INSERT ON ReservaAct
FOR EACH ROW
DECLARE
  contador NUMBER(5,0);
BEGIN
  -- Verifica si el DNI/Pasaporte del cliente de la tupla que se va a insertar tiene una habitación asignada
  SELECT COUNT(*) INTO contador FROM RegistroHotel r, HabReserva h WHERE r.CReserva = h.CReserva AND DNI_Pasaporte = :new.DNI_Pasaporte;
  IF (contador = 0) THEN
    -- Si dicho DNI/Pasaporte no tiene ninguna habitación asignada, se lanza una excepción
    RAISE_APPLICATION_ERROR(-20000, 'No se puede realizar la reserva de la actividad de ocio (El DNI/Pasaporte introducido no tiene ninguna habitación asignada)');
  END IF;
END;


CREATE OR REPLACE TRIGGER opinion_dni_cliente
	BEFORE
	INSERT ON OpinionAct
    FOR EACH ROW
DECLARE
	numero NUMBER(5,0);
BEGIN
	-- Si el dni y código están en una misma fila de ReservaAct, se permite opinar
	SELECT COUNT(*) INTO numero FROM ReservaAct ra WHERE ra.DNI_Pasaporte=:new.DNI_Pasaporte AND ra.ActOcio=:new.ActOcio;
	IF (numero = 0) THEN
		RAISE_APPLICATION_ERROR(-20600, :new.DNI_Pasaporte || 'El DNI/Pasaporte introducido no corresponde con ninguna reserva asociada a tal código');
	END IF;
END;



-- Realizados por Juan Manuel Rodríguez Gómez (Responsable del subsistema "Parking")

CREATE OR REPLACE TRIGGER no_reserva_parking
BEFORE INSERT ON ReservaParking
FOR EACH ROW
DECLARE
  contador NUMBER(5,0);
BEGIN
  -- Verifica si el DNI/Pasaporte del cliente de la tupla que se va a insertar tiene una habitación asignada
  SELECT COUNT(*) INTO contador FROM RegistroHotel r, HabReserva h WHERE r.CReserva = h.CReserva AND DNI_Pasaporte = :new.DNI_Pasaporte;
  IF (contador = 0) THEN
    -- Si dicho DNI/Pasaporte no tiene ninguna habitación asignada, se lanza una excepción
    RAISE_APPLICATION_ERROR(-20000, 'No se puede realizar la reserva de la plaza de parking (El DNI/Pasaporte introducido no tiene ninguna habitación asignada)');
  END IF;
END;



-- Realizados por Jesús García León (Responsable del subsistema "Mantenimiento de Instalaciones")

CREATE OR REPLACE TRIGGER precio_rep_no_modif
      BEFORE
      UPDATE OF PrecioReparacion ON Reparacion
      FOR EACH ROW
BEGIN
    RAISE_APPLICATION_ERROR (-20001, 'Esta tabla no se puede modificar, pruebe a borrar e insertar la tupla con el nuevo precio');
END;


CREATE OR REPLACE TRIGGER no_superar_presupuesto
      BEFORE
      INSERT ON Reparacion
      FOR EACH ROW
DECLARE
  precio_total NUMBER(8,2);
  presupuesto_total NUMBER(12,2) := 10000;
BEGIN
  SELECT SUM(PRECIOREPARACION) INTO PRECIO_TOTAL from REPARACION;
  precio_total := precio_total + :new.PRECIOREPARACION;
  IF (precio_total > presupuesto_total) THEN
    RAISE_APPLICATION_ERROR (-20600, 'La suma de los precios de reparación no puede superar el presupuesto total (10000€)');
  END IF;
END;
