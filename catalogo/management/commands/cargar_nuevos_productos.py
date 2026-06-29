import base64
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalogo.models import Categoria, Producto, ProductoImagen


BASE_DIR = Path(settings.BASE_DIR) / "nuevos productos"


PRODUCTOS = [
    {
        "nombre": "Kit de Emergencia Vial 3 en 1",
        "categoria": "Herramientas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 1.49.03 PM.jpeg"],
        "descripcion_corta": "Kit compacto para emergencias en carretera con cono, herramientas y accesorios de seguridad.",
        "descripcion": "Kit vial 3 en 1 pensado para llevar en el carro y responder ante pinchazos, fallas mecanicas o imprevistos. Incluye cono reflectivo, chaleco, guantes, cinta, remolque y herramientas esenciales en una caja organizada y facil de transportar.",
    },
    {
        "nombre": "Cámara WiFi Smart Net Pan Tilt",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-24 at 2.38.53 PM.jpeg"],
        "descripcion_corta": "Camara WiFi interior con movimiento horizontal y vertical, vision nocturna y audio bidireccional.",
        "descripcion": "Camara inteligente para hogar, negocio o monitoreo de mascotas. Permite ver en tiempo real desde el celular, cuenta con vision nocturna, conexion WiFi, intercomunicador de dos vias, soporte para memoria TF y movimiento pan/tilt para cubrir mejor el espacio.",
    },
    {
        "nombre": "Báscula Digital de Cocina",
        "categoria": "Cocina",
        "imagenes": ["WhatsApp Image 2026-06-24 at 3.11.30 PM.jpeg"],
        "descripcion_corta": "Bascula compacta con pantalla LCD, tara y medicion precisa para recetas y porciones.",
        "descripcion": "Bascula de cocina practica para reposteria, dietas, formulas e ingredientes precisos. Mide desde 1 g hasta 7 kg, permite cambiar unidades entre g y oz, cuenta con apagado automatico y funciona con pilas AAA.",
    },
    {
        "nombre": "Calentador de Agua con Purificador ZSW-D04",
        "categoria": "Cocina",
        "imagenes": ["WhatsApp Image 2026-06-24 at 3.25.26 PM.jpeg"],
        "descripcion_corta": "Calentador instantaneo para grifo con pantalla digital y sistema de filtrado.",
        "descripcion": "Solucion practica para obtener agua caliente al instante en la cocina o lavamanos. Su pantalla digital ayuda a revisar la temperatura y su sistema de purificacion mejora la calidad del agua para un uso diario mas comodo.",
    },
    {
        "nombre": "Correa Doble Giratoria con Linterna y Dispensador",
        "categoria": "Mascotas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 11.21.19 AM.jpeg"],
        "descripcion_corta": "Correa doble para pasear dos mascotas con cabezal giratorio, linterna LED y dispensador de bolsas.",
        "descripcion": "Correa doble ideal para paseos comodos con dos perros. El sistema giratorio ayuda a evitar enredos, la linterna LED mejora la visibilidad y el dispensador integrado permite llevar bolsas siempre a mano.",
    },
    {
        "nombre": "Taza Limpiadora de Patas para Mascotas",
        "categoria": "Mascotas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 11.23.51 AM.jpeg"],
        "descripcion_corta": "Limpiador automatico para patas de perros y gatos, practico para usar al llegar de paseo.",
        "descripcion": "Vaso limpiador para retirar suciedad de las patas de tu mascota sin esfuerzo. Su interior ayuda a limpiar suavemente, es facil de usar y evita llevar tierra o lodo al interior de la casa.",
    },
    {
        "nombre": "Cepillo Quitapelo Portátil para Mascotas",
        "categoria": "Mascotas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 11.24.22 AM.jpeg"],
        "descripcion_corta": "Cepillo manual sin electricidad para retirar pelo suelto y masajear a perros y gatos.",
        "descripcion": "Cepillo portatil de limpieza facil para mascotas. Retira pelo muerto y enredos, cuida la piel con cerdas suaves y permite liberar el pelo acumulado presionando el boton trasero.",
    },
    {
        "nombre": "Bebedero Eléctrico con Filtro para Mascotas",
        "categoria": "Mascotas",
        "imagenes": [
            "WhatsApp Image 2026-06-24 at 11.26.06 AM.jpeg",
            "WhatsApp Image 2026-06-24 at 11.32.53 AM.jpeg",
        ],
        "descripcion_corta": "Fuente electrica con filtro para mantener el agua fresca, limpia y en movimiento.",
        "descripcion": "Bebedero con sistema de filtracion multicapa para perros y gatos. Mantiene el agua en movimiento, ayuda a estimular la hidratacion, trabaja de forma silenciosa y esta fabricado con materiales seguros y faciles de limpiar.",
    },
    {
        "nombre": "Baño Sanitario Potty Patch para Mascotas",
        "categoria": "Mascotas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 11.37.43 AM.jpeg"],
        "descripcion_corta": "Tapete sanitario reutilizable con cesped artificial para entrenamiento en interiores.",
        "descripcion": "Bano practico para mascotas pequenas, balcones, apartamentos y viajes. Cuenta con cesped sintetico suave, bandeja lavable y estructura reutilizable para ayudar al entrenamiento de tu mascota.",
    },
    {
        "nombre": "Guante con Manguera para Bañar Mascotas",
        "categoria": "Mascotas",
        "imagenes": ["WhatsApp Image 2026-06-24 at 11.42.09 AM.jpeg"],
        "descripcion_corta": "Guante cepillador con manguera de 2 m para lavar, masajear y enjuagar al mismo tiempo.",
        "descripcion": "Kit para bano de mascotas con guante de silicona, manguera, valvula reguladora y conector universal. Permite distribuir el agua de forma uniforme mientras masajea y ayuda a retirar pelo suelto.",
    },
    {
        "nombre": "Ropero Organizador 3 en 1 para Lavandería",
        "categoria": "Hogar",
        "imagenes": [
            "WhatsApp Image 2026-06-25 at 2.28.39 PM (1).jpeg",
            "WhatsApp Image 2026-06-26 at 11.51.51 AM.jpeg",
        ],
        "descripcion_corta": "Organizador de lavanderia con tres compartimentos para separar ropa clara, oscura y de color.",
        "descripcion": "Ropero 3 en 1 con estructura metalica y bolsas removibles. Ayuda a organizar el lavado por colores, transportar ropa con facilidad y mantener lavanderias, banos o habitaciones mas ordenados.",
    },
    {
        "nombre": "Chaleco de Compresión Moldeador",
        "categoria": "Ejercicio",
        "imagenes": ["WhatsApp Image 2026-06-25 at 10.56.13 AM.jpeg"],
        "descripcion_corta": "Chaleco moldeador de compresion para soporte de espalda y uso diario o deportivo.",
        "descripcion": "Chaleco ergonomico de compresion para mejorar la postura y brindar soporte durante entrenamientos, levantamiento de pesas o actividades diarias. Su tela elastica y transpirable se adapta al cuerpo.",
    },
    {
        "nombre": "Almohadilla Calefactora para Hombro",
        "categoria": "Ejercicio",
        "imagenes": ["WhatsApp Image 2026-06-25 at 10.59.40 AM.jpeg"],
        "descripcion_corta": "Soporte termico ajustable para hombro con tres niveles de temperatura.",
        "descripcion": "Almohadilla para hombro con calor terapeutico y correa ajustable. Ayuda a relajar hombros y musculos, cuenta con niveles bajo, medio y alto, y es comoda para uso en casa u oficina.",
    },
    {
        "nombre": "Rodillera de Soporte ND-528",
        "categoria": "Ejercicio",
        "imagenes": ["WhatsApp Image 2026-06-25 at 11.01.04 AM.jpeg"],
        "descripcion_corta": "Rodillera ajustable de neopreno para soporte, estabilidad y comodidad durante el movimiento.",
        "descripcion": "Rodillera deportiva con diseno rotuliano abierto, correas ajustables y material transpirable. Ayuda a proteger, estabilizar y brindar soporte durante entrenamientos, running, ciclismo o gimnasio.",
    },
    {
        "nombre": "Rodillera Térmica Recargable",
        "categoria": "Ejercicio",
        "imagenes": ["WhatsApp Image 2026-06-25 at 11.03.11 AM.jpeg"],
        "descripcion_corta": "Rodillera con calor terapeutico, bateria recargable y tres niveles de temperatura.",
        "descripcion": "Rodillera termica portatil para deportistas y personas activas. Ofrece calor en niveles bajo, medio y alto, ayuda a relajar la zona de la rodilla y es ajustable para uso diario.",
    },
    {
        "nombre": "Almohada Cervical Masajeadora en U",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-25 at 11.27.29 AM.jpeg"],
        "descripcion_corta": "Almohada cervical en U con masaje, calor e intensidad ajustable.",
        "descripcion": "Masajeador acolchado para cuello y hombros con nodos integrados y control de modo. Ideal para casa, oficina o viajes, ayuda a relajar la tension y ofrece una experiencia comoda de descanso.",
    },
    {
        "nombre": "Manta Térmica Eléctrica con Control",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-25 at 11.31.01 AM.jpeg"],
        "descripcion_corta": "Manta electrica con control digital, calor constante y apagado automatico.",
        "descripcion": "Manta termica para alivio calido en abdomen, espalda, hombros o cabeza. Cuenta con tres niveles de temperatura, tela suave y comoda, funda lavable y bajo consumo de energia.",
    },
    {
        "nombre": "Arrancador de Batería con Compresor Power Start Pro",
        "categoria": "Herramientas",
        "imagenes": [
            "WhatsApp Image 2026-06-25 at 12.51.05 PM.jpeg",
            "WhatsApp Image 2026-06-25 at 12.55.37 PM.jpeg",
        ],
        "descripcion_corta": "Equipo 5 en 1 para arrancar bateria, inflar llantas, iluminar y cargar dispositivos.",
        "descripcion": "Arrancador portatil con compresor de aire, powerbank USB, linterna LED y luces de emergencia. Ideal para autos, motos y camionetas, pensado para llevar en carretera y responder ante imprevistos.",
    },
    {
        "nombre": "Organizador de Lavadora",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-26 at 1.08.33 PM.jpeg"],
        "descripcion_corta": "Estante organizador para colocar sobre la lavadora y aprovechar mejor el espacio.",
        "descripcion": "Organizador metalico para lavanderia, ideal para jabon, toallas y accesorios. Su diseno practico permite ordenar productos de uso diario y optimizar espacios pequenos.",
    },
    {
        "nombre": "Mopa Spray 360 de Microfibra",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-26 at 2.14.08 PM.jpeg"],
        "descripcion_corta": "Mopa plana con spray, giro 360 y pad de microfibra para limpieza rapida.",
        "descripcion": "Trapeador ligero y comodo con funcion spray para rociar y limpiar en un solo paso. Su cabezal giratorio permite llegar a rincones y debajo de muebles sin esfuerzo.",
    },
    {
        "nombre": "Pistola de Anclaje Profesional",
        "categoria": "Herramientas",
        "imagenes": ["WhatsApp Image 2026-06-26 at 2.57.36 PM.jpeg"],
        "descripcion_corta": "Herramienta de fijacion rapida para concreto, ladrillo, acero, madera y bloque.",
        "descripcion": "Pistola de anclaje con estuche y accesorios para trabajos de instalacion, construccion y reparacion. Incluye gafas de seguridad, clavos con arandela, resortes de repuesto, cepillo de limpieza y llave.",
    },
    {
        "nombre": "Cepillo Secador Remington Avocado 3D Power",
        "categoria": "Belleza",
        "imagenes": ["WhatsApp Image 2026-06-26 at 5.25.45 PM.jpeg"],
        "descripcion_corta": "Cepillo secador y modelador Remington con potencia 3000 W.",
        "descripcion": "Cepillo secador para secar, moldear y dar suavidad al cabello en una sola herramienta. Ideal para rutina diaria, brinda brillo y acabado natural con facil manejo.",
    },
    {
        "nombre": "Set de Peinado 2 en 1",
        "categoria": "Belleza",
        "imagenes": ["WhatsApp Image 2026-06-26 at 5.43.59 PM.jpeg"],
        "descripcion_corta": "Herramienta 2 en 1 para alisar y rizar el cabello en minutos.",
        "descripcion": "Set de peinado con rizador y cepillo alisador en una herramienta practica. Diseno ligero para uso diario, ideal para crear ondas, rizos o alisados segun el look que prefieras.",
    },
    {
        "nombre": "Peine Térmico High Heat",
        "categoria": "Belleza",
        "imagenes": ["WhatsApp Image 2026-06-26 at 6.10.07 PM.jpeg"],
        "descripcion_corta": "Peine termico ceramico para alisar y peinar el cabello con facilidad.",
        "descripcion": "Peine electrico de calentamiento rapido para alisar y peinar al mismo tiempo. Ideal para uso diario y acabado profesional en casa.",
    },
    {
        "nombre": "Secador Plegable Premium",
        "categoria": "Belleza",
        "imagenes": ["WhatsApp Image 2026-06-26 at 7.46.38 PM.jpeg"],
        "descripcion_corta": "Secador compacto y plegable, facil de llevar y usar en la rutina diaria.",
        "descripcion": "Secador de cabello portatil con diseno compacto. Pensado para casa, viajes o gimnasio, combina practicidad, estilo y facilidad de almacenamiento.",
    },
    {
        "nombre": "Smartwatch Fit Pro",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.38 AM.jpeg"],
        "descripcion_corta": "Smartwatch deportivo para monitoreo de salud, actividad diaria y notificaciones.",
        "descripcion": "Reloj inteligente ligero para entrenamientos y vida diaria. Permite revisar ritmo cardiaco, pasos, calorias y notificaciones, con bateria de larga duracion y diseno resistente al agua.",
    },
    {
        "nombre": "Combo Smartwatch D99 Plus 7+4",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.39 AM.jpeg"],
        "descripcion_corta": "Combo con smartwatch, audifonos, parlante portatil, cargador inalambrico y correas.",
        "descripcion": "Kit D99 Plus para mantenerte conectado desde la muneca. Incluye reloj inteligente, audifonos inalambricos, parlante portatil, cargador inalambrico y correas intercambiables para diferentes estilos.",
    },
    {
        "nombre": "Combo Smartwatch Rock-003 18 en 1",
        "categoria": "Tecnología",
        "imagenes": [
            "WhatsApp Image 2026-06-26 at 10.43.40 AM.jpeg",
            "WhatsApp Image 2026-06-26 at 10.43.41 AM (1).jpeg",
        ],
        "descripcion_corta": "Combo 18 en 1 con smartwatch, audifonos, cargador inalambrico y correas intercambiables.",
        "descripcion": "Set Rock-003 para deporte y uso diario. Incluye smartwatch con pantalla AMOLED, monitoreo de salud, modos deportivos, audifonos inalambricos, cargador, correas y accesorios para mantenerse conectado.",
    },
    {
        "nombre": "Smartwatch C900 ProMax",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.41 AM.jpeg"],
        "descripcion_corta": "Smartwatch de alto rendimiento con llamadas Bluetooth y pantalla HD 2.19 pulgadas.",
        "descripcion": "Reloj inteligente para entrenar, trabajar y mantenerse conectado. Cuenta con monitoreo de salud, modos deportivos, llamadas Bluetooth, notificaciones en tiempo real y diseno moderno compatible con iOS y Android.",
    },
    {
        "nombre": "Smartwatch T900 Pro Max",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.42 AM.jpeg"],
        "descripcion_corta": "Smartwatch con llamadas Bluetooth, salud 24/7 y mas de 100 modos deportivos.",
        "descripcion": "Reloj inteligente T900 Pro Max para actividad diaria. Permite llamadas desde el reloj, registro deportivo, reproduccion de musica, notificaciones y bateria de hasta 5 dias de uso.",
    },
    {
        "nombre": "Smartwatch T300 Ultra",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.43 AM.jpeg"],
        "descripcion_corta": "Smartwatch con pantalla grande 2.01 pulgadas, llamadas Bluetooth y control de camara.",
        "descripcion": "Reloj inteligente T300 Ultra con pantalla amplia, monitoreo de salud 24/7, mas de 100 modos deportivos, notificaciones, clima, musica, control de camara y resistencia al agua.",
    },
    {
        "nombre": "Smartwatch T900 Ultra 2 Big",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.44 AM.jpeg"],
        "descripcion_corta": "Smartwatch de pantalla grande con llamadas Bluetooth, musica y notificaciones.",
        "descripcion": "T900 Ultra 2 Big ofrece una experiencia de pantalla amplia para el dia a dia. Incluye monitoreo de salud, modos deportivos, llamadas Bluetooth, musica, clima, control de camara y bateria de larga duracion.",
    },
    {
        "nombre": "Smartwatch M50 Ultra 2 con Audifonos",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 10.43.45 AM.jpeg"],
        "descripcion_corta": "Combo M50 Ultra 2 con smartwatch, audifonos, correa adicional y cable magnetico.",
        "descripcion": "Smartwatch para un estilo de vida activo y conectado. Permite llamadas Bluetooth, reproduccion de musica, mensajes, monitoreo cardiaco, sueno, pasos, calorias y notificaciones.",
    },
    {
        "nombre": "Recipiente Hermético Transparente para Alimentos",
        "categoria": "Cocina",
        "imagenes": [
            "WhatsApp Image 2026-06-26 at 10.55.52 AM.jpeg",
            "WhatsApp Image 2026-06-26 at 10.55.53 AM.jpeg",
        ],
        "descripcion_corta": "Recipiente transparente con cierre hermetico para conservar alimentos frescos.",
        "descripcion": "Contenedor reutilizable para frutas, verduras, almuerzos y porciones. Es libre de BPA, apto para congelador, apto para microondas sin tapa, facil de lavar y practico para organizar la nevera.",
    },
    {
        "nombre": "Freidora de Aire Zoky So 8L",
        "categoria": "Cocina",
        "imagenes": ["WhatsApp Image 2026-06-26 at 11.11.35 AM.jpeg"],
        "descripcion_corta": "Air fryer extra grande de 8 litros y 2400 W con control digital.",
        "descripcion": "Freidora de aire de gran capacidad para preparar alimentos crujientes con menos aceite. Cuenta con panel digital, piezas desmontables, tecnologia de coccion uniforme y capacidad ideal para familias.",
    },
    {
        "nombre": "Proyector de Luz Astronauta",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 11.30.49 AM.jpeg"],
        "descripcion_corta": "Proyector de galaxias y estrellas con luces LED, musica y control remoto.",
        "descripcion": "Lampara proyectora con forma de astronauta para transformar habitaciones en una galaxia. Incluye control remoto, cabezal giratorio 360, luces de colores y musica integrada.",
    },
    {
        "nombre": "Bomba de Vacío Inteligente para Bolsas",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-26 at 11.32.32 AM.jpeg"],
        "descripcion_corta": "Bomba electrica compacta para extraer aire de bolsas de almacenamiento.",
        "descripcion": "Bomba de vacio portatil con operacion de un boton y detencion automatica. Ayuda a reducir volumen hasta un 80 por ciento, es facil de transportar e ideal para ropa, almohadas y viajes.",
    },
    {
        "nombre": "Bandeja Barbecue Tray Antiadherente",
        "categoria": "Cocina",
        "imagenes": ["WhatsApp Image 2026-06-26 at 11.39.31 AM.jpeg"],
        "descripcion_corta": "Bandeja antiadherente portatil de 34 cm para asar carnes, mariscos y verduras.",
        "descripcion": "Bandeja para parrilla con superficie antiadherente, asas laterales y distribucion uniforme del calor. Es ligera, facil de limpiar y apta para contacto con alimentos.",
    },
    {
        "nombre": "Envoltura Térmica para Rodilla con Masaje",
        "categoria": "Ejercicio",
        "imagenes": ["WhatsApp Image 2026-06-26 at 11.48.05 AM.jpeg"],
        "descripcion_corta": "Envoltura ajustable con calor, vibracion y bateria recargable para la rodilla.",
        "descripcion": "Soporte termico para rodilla con masaje por vibracion y tres niveles de calor. Ayuda a relajar, mejorar la circulacion y brindar bienestar en casa, oficina o despues del ejercicio.",
    },
    {
        "nombre": "Contadora de Billetes Profesional",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 12.11.24 PM.jpeg"],
        "descripcion_corta": "Maquina profesional para conteo rapido de billetes con deteccion UV y magnetica.",
        "descripcion": "Contadora de billetes para negocios y oficinas. Ofrece conteo rapido y preciso, pantalla LED externa, luz ultravioleta y deteccion magnetica para apoyar el control de efectivo.",
    },
    {
        "nombre": "Handy Counter Contadora Portátil",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-26 at 12.11.35 PM.jpeg"],
        "descripcion_corta": "Contadora compacta de dinero con funcion ADD y pantalla LED.",
        "descripcion": "Contadora portatil para billetes ordenados, ideal para negocios, supermercados, restaurantes, oficinas y bancos. Su funcion ADD acumula conteos y ayuda a ahorrar tiempo.",
    },
    {
        "nombre": "Perchero Multifuncional con Ruedas",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-26 at 12.35.47 PM.jpeg"],
        "descripcion_corta": "Perchero doble para ropa, zapatos, bolsos y sacos con diseno movil.",
        "descripcion": "Perchero multifuncional para organizar prendas y accesorios en habitaciones o closets. Su estructura con ruedas facilita moverlo y aprovechar mejor el espacio.",
    },
    {
        "nombre": "Zapatero Multifuncional 5 Niveles",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-26 at 12.51.44 PM.jpeg"],
        "descripcion_corta": "Zapatero de 5 niveles para organizar varios pares de forma practica y elegante.",
        "descripcion": "Organizador de zapatos con estructura compacta, facil de armar y adecuado para habitaciones, entradas o closets. Ayuda a ahorrar espacio y mantener el calzado visible y ordenado.",
    },
    {
        "nombre": "Pinza Onduladora Professional Perm",
        "categoria": "Belleza",
        "imagenes": [
            "WhatsApp Image 2026-06-27 at 1.03.37 PM.jpeg",
            "WhatsApp Image 2026-06-27 at 12.59.01 PM.jpeg",
        ],
        "descripcion_corta": "Pinza onduladora profesional para rizos definidos y ondas duraderas.",
        "descripcion": "Onduladora de calentamiento rapido para crear rizos con acabado de salon. Facil de usar, ideal para peinados diarios o eventos, con diseno practico para definir ondas.",
    },
    {
        "nombre": "Frasco Atomizador Rellenable 100 ml",
        "categoria": "Hogar",
        "imagenes": ["WhatsApp Image 2026-06-27 at 1.53.51 PM.jpeg"],
        "descripcion_corta": "Atomizador de vidrio rellenable para aceites, vinagres, limpiadores o perfumes.",
        "descripcion": "Frasco atomizador reutilizable con rociado fino y uniforme. Incluye embudo para llenar sin derrames, diseno moderno y capacidad de 100 ml para cocina, hogar o trabajo.",
    },
    {
        "nombre": "Licuadora Portátil Recargable 400 ml",
        "categoria": "Licuadora",
        "imagenes": ["WhatsApp Image 2026-06-27 at 11.31.03 AM.jpeg"],
        "descripcion_corta": "Licuadora portatil con vaso de 400 ml, seis cuchillas y bateria recargable USB.",
        "descripcion": "Licuadora compacta para preparar jugos y batidos en segundos. Cuenta con cuchillas de acero inoxidable, vaso portatil, bateria recargable y materiales seguros libres de BPA.",
    },
    {
        "nombre": "Traje Impermeable para Moto y Bicicleta",
        "categoria": "Herramientas",
        "imagenes": ["WhatsApp Image 2026-06-27 at 11.38.39 AM.jpeg"],
        "descripcion_corta": "Traje impermeable reflectivo para moto o bicicleta con capucha ajustable.",
        "descripcion": "Conjunto para lluvia con chaqueta y pantalon, cintas reflectantes, punos elasticos y material ligero. Ideal para trayectos en moto o bicicleta bajo lluvia intensa.",
    },
    {
        "nombre": "Pijama Cubierta Impermeable para Moto",
        "categoria": "Herramientas",
        "imagenes": ["WhatsApp Image 2026-06-27 at 11.38.47 AM.jpeg"],
        "descripcion_corta": "Cubierta impermeable para proteger motos contra lluvia, sol, polvo y humedad.",
        "descripcion": "Pijama protectora para motos con material resistente, costuras reforzadas, elastico ajustable y ojales de seguridad. Compatible con la mayoria de motos deportivas, urbanas y naked.",
    },
    {
        "nombre": "Secador Profesional BSK-NOVA",
        "categoria": "Belleza",
        "imagenes": ["WhatsApp Image 2026-06-27 at 12.16.47 PM.jpeg"],
        "descripcion_corta": "Secador profesional de cabello con diseno elegante para casa o salon.",
        "descripcion": "Secador BSK-NOVA para secado rapido y rutina diaria. Combina potencia, estilo y practicidad, ideal para uso en casa o salon de belleza.",
    },
    {
        "nombre": "TV Stick 10K Streaming",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-27 at 12.26.06 PM.jpeg"],
        "descripcion_corta": "Dispositivo streaming tipo TV stick para apps, canales, peliculas y series.",
        "descripcion": "TV Stick compacto con control remoto, adaptadores y guia de uso. Permite convertir el televisor en un centro de entretenimiento con aplicaciones, peliculas, series y contenido en linea.",
    },
    {
        "nombre": "Mini Proyector LED Portátil 1080P",
        "categoria": "Tecnología",
        "imagenes": ["WhatsApp Image 2026-06-27 at 12.27.30 PM.jpeg"],
        "descripcion_corta": "Proyector LED compacto compatible con 1080P, HDMI, USB, AV y tarjeta TF.",
        "descripcion": "Mini proyector portatil para peliculas, videojuegos, presentaciones y eventos al aire libre. Ofrece altavoz integrado, enfoque manual, bajo consumo y pantalla proyectada de gran tamano.",
    },
    {
        "nombre": "Seguro para Volante con Cable de Acero",
        "categoria": "Herramientas",
        "imagenes": ["WhatsApp Image 2026-06-27 at 12.33.03 PM.jpeg"],
        "descripcion_corta": "Seguro antirrobo para volante con cable de acero templado y ajuste universal.",
        "descripcion": "Bloqueo para volante facil de instalar, compacto y resistente. Ayuda a disuadir robos, se ajusta a la mayoria de vehiculos y se guarda facilmente en la guantera o consola.",
    },
]


def encode_image(path):
    with path.open("rb") as image_file:
        datos = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{datos}"


class Command(BaseCommand):
    help = "Carga productos nuevos desde la carpeta nuevos productos, evitando duplicados por nombre/slug."

    def handle(self, *args, **options):
        created = []
        skipped = []
        missing = []

        for data in PRODUCTOS:
            slug = slugify(data["nombre"])
            exists = Producto.objects.filter(slug=slug).exists() or Producto.objects.filter(
                nombre__iexact=data["nombre"]
            ).exists()

            if exists:
                skipped.append(data["nombre"])
                continue

            categoria, _ = Categoria.objects.get_or_create(nombre=data["categoria"])
            producto = Producto.objects.create(
                nombre=data["nombre"],
                categoria=categoria,
                precio=None,
                descripcion_corta=data["descripcion_corta"],
                descripcion=data["descripcion"],
                disponible=True,
            )

            for orden, filename in enumerate(data["imagenes"]):
                path = BASE_DIR / filename
                if not path.exists():
                    missing.append(f"{data['nombre']}: {filename}")
                    continue

                ProductoImagen.objects.create(
                    producto=producto,
                    imagen_data=encode_image(path),
                    orden=orden,
                )

            created.append(data["nombre"])

        self.stdout.write(self.style.SUCCESS(f"Productos creados: {len(created)}"))
        for name in created:
            self.stdout.write(f"  + {name}")

        self.stdout.write(self.style.WARNING(f"Productos omitidos por existir: {len(skipped)}"))
        for name in skipped:
            self.stdout.write(f"  = {name}")

        if missing:
            self.stdout.write(self.style.ERROR(f"Imagenes no encontradas: {len(missing)}"))
            for item in missing:
                self.stdout.write(f"  ! {item}")
