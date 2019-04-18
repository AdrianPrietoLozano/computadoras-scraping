DROP DATABASE proyecto_computadoras;
CREATE DATABASE proyecto_computadoras;
USE proyecto_computadoras;


CREATE TABLE ram(
	id INT PRIMARY KEY AUTO_INCREMENT,
	tipo VARCHAR(20),
	capacidad INT
);

CREATE TABLE procesador(
	id INT PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(50),
	marca VARCHAR(25),
	nombre_reducido VARCHAR(50)
);

CREATE TABLE sistema_operativo(
	id INT PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(25)
);

CREATE TABLE almacenamiento(
	id INT PRIMARY KEY AUTO_INCREMENT,
	capacidad INT
);


CREATE TABLE computadora(
	id INT PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(100),
	precio FLOAT,
	marca VARCHAR(20),
	opcion_compra VARCHAR(150),
	id_ram INT,
	id_procesador INT,
	id_so INT,
	id_almacenamiento INT,
	FOREIGN KEY(id_ram) REFERENCES ram(id),
	FOREIGN KEY(id_procesador) REFERENCES procesador(id),
	FOREIGN KEY(id_so) REFERENCES sistema_operativo(id),
	FOREIGN KEY(id_almacenamiento) REFERENCES almacenamiento(id)
);

CREATE TABLE recomendados(
	id INT PRIMARY KEY AUTO_INCREMENT,
	id_computadora INT,
	FOREIGN KEY(id_computadora) REFERENCES computadora(id)
);

CREATE TABLE estadisticas(
	id_computadora INT,
	contador INT,
	FOREIGN KEY(id_computadora) REFERENCES computadora(id)
);