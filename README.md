# Veterinaria Amigos Peludos
## Realizado por:

- Alejandra David
- Cristian Baena
- Gabriel Franco

## Funcionalidades:

- **Menú de interacción:** Al ejecutar la aplicación nos encontramos con una interfaz de consola que nos enseña las opciones
disponibles en esta, las cuales son: `Registrar mascota`, `Registrar consulta`, `Listar Mascotas`, `Ver Historial De Consultas` y `Salir De La Aplicación`.

- **Registrar Mascota:** Esta función se encarga de capturar la información de la mascota y su dueño para registrarla independientemente en la clase correspondiente, contiene validaciones para que la información capturada sea consistente con los datos solicitados.

- **Registrar Consulta:** Esta función se encarga de registrar consultas solo para mascotas existentes en el sistema, si una mascota no se encuentra registrada en el sistema, no podrá registrar una nueva consulta. No contiene validaciones de fecha por motivos de simplicidad y experiencia de usuario, ya que al no contar con persistencia de datos, no se considera relevante añadir validaciones de fecha en este proyecto, facilitando el ingreso de ua fecha en el formato que el usuario lo decida.

- **Listar Mascotas:** Esta función se encarga de desplegar en pantalla todas la información de las mascotas regitradas en el sistema junto con la información de su dueño, separando cada mascota de forma individual para facilitar su legibilidad.

- **Ver Historial De Consultas:** Esta función se encarga de desplegar en pantalla las consultas registradas para una mascota en específico, utilizando en nombre de la mascota como criterio específico, separando cada consulta de forma individual para así obtener una mejor legibilidad. Si la mascota en cuestión no tiene consultas registradas, se mostrará un mensaje en pantalla indicando que la mascota no tiene ninguna consulta en su registro.

- **Salir de la aplicación:** Al hacer uso de esta función, la aplicación se detendrá por completo y su memoria se reiniciará, eliminando toda la información registrada, ya que este proyecto no cuenta con persistencia de datos.

## Construido con:

[Python 3.11.9]