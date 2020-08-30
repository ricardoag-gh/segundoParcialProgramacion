Estudiantes : Ricardo Aguilar González, Pablo Salazar Mora, Joseph Camacho

Curso : Programación Avanzada

Gith Hub Link : https://github.com/ricardoag-gh/segundoParcialProgramacion

Segundo Parcial
-----------------

Alcance del proyecto:

** Login

- Se permite crear usuarios. Los usuarios pueden ser de dos tipos : administrador y no administrador. El usuario administrador tendrá permisos para agregar otros usuarios, convertir usuarios existentes en "Administradores", eliminar usuarios y listar todos los usuarios o listar usuarios por ID. 

Los usuarios que se crean por default serán no administradores, por lo que este tipo de usuarios recibirá un mensaje indicando que no están autorizados cuando intenten : eliminar otros usuarios, listar todos los usuarios, o listar usuarios por ID.

Una vez un usuario se registra, para iniciar sesión con el debemos ir a la sección de "Authorization" en el Postman y seleccionar "Basic Auth" como tipo de autorización, posteriormente a esto se debe ingresar el usuario y el password. De introducir correctamente el password se generara un Token, que posteriormente agregaremos al Key "x-access-token" en el header de postman(Se debe crear este key). Si el password o el usuario no son introducidos, o alguno de estos dos datos o ambos es incorrecto, se le indicará al usuario.

Como ejemplo de usuario administrador puede usar los siguientes credenciales :



Como ejemplo de usuario administrador puede usar los siguientes credenciales :

Username : User4

Password : passwordtest4



Y usuario no administrador :

Username : User15

Password : passwordtest15


** Si desea agregar un nuevo usuario, solo agregue el siguiente código en el body de Postman : Asegurese de seleccionar la opcion "raw" y JSON. 

{"username" : "User15", "password" : "passwordtest15"}

------------------------------------------------

** Agregar comida

Ya sea que el usuario es administrador o no, este podrá ingresar alimentos con una descripción, ademas podrá editarlos, para que su estado "eaten" pase de verdadero a false, y si desea puede eliminar el producto. De igual forma el usuario podrá listar todos sus productos ingresados y listarlos por ID, mas no podrá ver productos de otros usuarios aunque sean administradores. 


------------------------------------------------
Instrucciones:

El siguiente proyecto se debe correr desde el archivo 'main.py', y es necesario el uso del software "Postman" que se puede descargar desde el siguiente URL "https://www.postman.com/downloads/" para correr las peticiones o solicitudes HTTP. 

1- Inicialmente se recomienda loguearse : 

Ruta : http://127.0.0.1:5000/login

Una vez se loguea, si los credenciales son los correctos, recibirá un token, este ingréselo como valor del key "x-access-token", en la sección Headers de Postman. 

2- Posteriormente podrá realizar las siguientes acciones, este será tomando en cuenta que se ha fogueado con un usuario administrador :


- Ver todos los usuarios : http://127.0.0.1:5000/user/all 

--> Postman : GET



- Ver un usuario en especifico(Especificar el "public_id" del usuario a consultar ) :

http://127.0.0.1:5000/user/86ff1184-97c4-4fa2-bf43-a1c95ca472d3 

--> Postman : GET




- Hacer un usuario administrador(Agregar el public_id del usuario que desea hace admin ) : http://127.0.0.1:5000/user/404cee97-5f82-48f7-9a0d-f43154463e71 

--> Postman : PUT




- Eliminar un usuario(Especificar el public_id del usuario a borrar) : http://127.0.0.1:5000/user/404cee97-5f82-48f7-9a0d-f43154463e71 

--> Postman : DELETE




- Agregar usuario : http://127.0.0.1:5000/user/add

--> Postman : POST

Estructura necesaria para agregar user : 
{"username" : "User16", "password" : "passwordtest16"}


En cuanto a productos estos son los URLs a utilizar :




- Ver todos los productos : http://127.0.0.1:5000/food/all

--> Postman : GET




- Ver producto por ID(Especificar el id del producto a buscar) : http://127.0.0.1:5000/food/1

--> Postman : GET




- Agregar alimento : http://127.0.0.1:5000/food

--> Postman : POST

Estructura necesaria para el Header en Postman:

{"description" : "Cereal: Granos."}




-Eliminar producto(Especificar el producto a eliminar) : http://127.0.0.1:5000/food/9
--> Postman : DELETE



- Cambiar estado de comido o no (Especificar el id del producto a actualizar):http://127.0.0.1:5000/food/9

--> Postman : PUT




Para efectos demostrativos se incluye el siguiente video explicando como correr el proyecto por Postman : https://uamcrnet-my.sharepoint.com/:v:/g/personal/ricardo_aguilar1_uamcr_net/EcIFO66E4-xIp0qAyP70OQoB_p3z9h03wi4qnp-WS_hzIA?e=h4XcAP








