import base64
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from catalogo.models import Categoria, Producto, ProductoImagen

IMGS_DIR = Path(__file__).resolve().parent.parent.parent.parent / 'datos' / 'imagenes'

CATEGORIAS = [
    ('Cocina y Electrodomésticos', 1),
    ('Tecnología y Gadgets', 2),
    ('Salud y Bienestar', 3),
    ('Belleza y Cuidado Personal', 4),
    ('Deportes y Fitness', 5),
    ('Hogar y Organización', 6),
    ('Herramientas y Vehículos', 7),
    ('Mascotas', 8),
    ('Bebé y Maternidad', 9),
    ('Juguetes y Entretenimiento', 10),
]

# (nombre, categoria, descripcion_corta, imagen_principal, [imagenes_extra])
PRODUCTOS = [
    # ── Cocina y Electrodomésticos ──────────────────────────────────────────
    (
        'Máquina para Crispetas Minijoy',
        'Cocina y Electrodomésticos',
        'Crispetas en 3 minutos sin aceite. Fácil de usar con un solo botón.',
        'IMG-20260517-WA0076.jpg', [],
    ),
    (
        'Batidora de Mano Sokany 400W',
        'Cocina y Electrodomésticos',
        'Mezcla, bate y amasa. Motor 400W, 5 velocidades + turbo, accesorios intercambiables.',
        'IMG-20260517-WA0082.jpg', ['IMG-20260517-WA0140.jpg'],
    ),
    (
        'Olla de Vidrio con Tapa Osito 1L',
        'Cocina y Electrodomésticos',
        'Vidrio borosilicato resistente, tapa con diseño de osito. Apta para microondas, 1 litro.',
        'IMG-20260517-WA0083.jpg', ['IMG-20260517-WA0153.jpg'],
    ),
    (
        'Parrilla Eléctrica Sokany SK-223 Grill Maker',
        'Cocina y Electrodomésticos',
        'Parrilla 2 en 1: abierta o cerrada. 850W, placas antiadherentes, apertura 180°.',
        'IMG-20260517-WA0089.jpg', ['IMG-20260517-WA0173.jpg', 'WhatsApp Image 2026-05-17 at 2.52.57 PM.jpeg'],
    ),
    (
        'Estufa Eléctrica Doble Sokany SK-5102',
        'Cocina y Electrodomésticos',
        'Doble quemador 2000W, calentamiento rápido, superficie de acero inoxidable fácil de limpiar.',
        'IMG-20260517-WA0113.jpg', [],
    ),
    (
        'Máquina para Granizados Electric Mein Mein',
        'Cocina y Electrodomésticos',
        'Tritura hielo al instante. Ideal para granizados, batidos y bebidas frías.',
        'IMG-20260517-WA0123.jpg', [],
    ),
    (
        'Máquina de Sellado al Vacío Vacuum Sealer',
        'Cocina y Electrodomésticos',
        'Conserva alimentos frescos por más tiempo. Operación con un solo botón, incluye 10 bolsas.',
        'IMG-20260517-WA0135.jpg', [],
    ),
    (
        'Tabla de Corte en Acero Inoxidable',
        'Cocina y Electrodomésticos',
        'Higiénica, resistente a golpes y rayones. No absorbe olores ni bacterias, con asa para colgar.',
        'IMG-20260517-WA0151.jpg', [],
    ),
    (
        'Hervidora de Huevos Diseño Gallina',
        'Cocina y Electrodomésticos',
        'Cocción al vapor para hasta 7 huevos. Apagado automático con indicador LED.',
        'IMG-20260517-WA0146.jpg', ['IMG-20260517-WA0147.jpg'],
    ),
    (
        'Donut Maker – 7 Donas Perfectas',
        'Cocina y Electrodomésticos',
        'Prepara 7 donas en minutos. Placas antiadherentes, calentamiento rápido y uniforme.',
        'IMG-20260517-WA0162.jpg', [],
    ),
    (
        'Exprimidor Eléctrico de Cítricos USB',
        'Cocina y Electrodomésticos',
        'Jugo fresco con un solo botón. Filtrado eficiente, recargable por USB.',
        'IMG-20260517-WA0163.jpg', [],
    ),
    (
        'Crepera Eléctrica Antiadherente',
        'Cocina y Electrodomésticos',
        'Crepes perfectas en segundos. Superficie antiadherente, calentamiento rápido, fácil de limpiar.',
        'IMG-20260517-WA0165.jpg', [],
    ),
    (
        'Extractor de Jugos Sokany 800W',
        'Cocina y Electrodomésticos',
        'Extractor de jugos potente 800W, 2 velocidades. Conserva vitaminas y nutrientes.',
        'IMG-20260517-WA0171.jpg', [],
    ),
    (
        'Estufa de Gas Portátil Sokany SK-07005',
        'Cocina y Electrodomésticos',
        'Estufa de gas 2.2kW, encendido automático, tapa protectora. Ideal para casa, camping y viajes.',
        'IMG-20260517-WA0172.jpg', [],
    ),

    # ── Tecnología y Gadgets ─────────────────────────────────────────────────
    (
        'Gafas Inteligentes con Cámara HD',
        'Tecnología y Gadgets',
        'Graba video HD y toma fotos manos libres. Micrófono integrado, batería 2 horas.',
        'IMG-20260517-WA0079.jpg', [],
    ),
    (
        'Mini Cámara WiFi A9 HD 1080P',
        'Tecnología y Gadgets',
        'Vigilancia discreta HD 1080P con WiFi. Visión nocturna, detección de movimiento, imán integrado.',
        'IMG-20260517-WA0084.jpg', [],
    ),
    (
        'Lentes Inteligentes G58 – Audio Bluetooth 5.4',
        'Tecnología y Gadgets',
        'Escucha música y responde llamadas sin audífonos. Bluetooth 5.4, UV400, hasta 6 horas.',
        'IMG-20260517-WA0085.jpg', ['IMG-20260517-WA0141.jpg'],
    ),
    (
        'Lentes Inteligentes con IA AiMB-S1',
        'Tecnología y Gadgets',
        'Asistente IA integrado, traducción en tiempo real, cámara, llamadas y música. Hasta 8 horas.',
        'IMG-20260517-WA0087.jpg', [],
    ),
    (
        'Pilas Recargables Ironbat AA + AAA con Cargador',
        'Tecnología y Gadgets',
        '2 pilas AA + 2 pilas AAA precargadas + cargador rápido. Ecológicas y reutilizables.',
        'IMG-20260517-WA0109.jpg', [],
    ),
    (
        'Cámara Espía en Bombillo WiFi HD 1080P',
        'Tecnología y Gadgets',
        'Cámara de seguridad oculta en bombillo E27. HD 1080P, visión nocturna, detección movimiento.',
        'IMG-20260517-WA0132.jpg', [],
    ),
    (
        'Radios Baofeng BF-888S – Par de Walkie-Talkies',
        'Tecnología y Gadgets',
        'Comunicación de hasta 5 km, 16 canales UHF/VHF, batería 12 horas. Set de 2 unidades.',
        'IMG-20260517-WA0136.jpg', ['IMG-20260517-WA0137.jpg'],
    ),
    (
        'Megáfono de Alto Alcance Recargable',
        'Tecnología y Gadgets',
        'Sonido potente y claro, batería recargable hasta 6 horas. Disponible en rojo y azul.',
        'IMG-20260517-WA0152.jpg', [],
    ),
    (
        'Cámara de Seguridad Solar Exterior Smart Home',
        'Tecnología y Gadgets',
        'Cámara WiFi solar para exteriores. HD 1080P, audio bidireccional, detección de movimiento.',
        'IMG-20260517-WA0169.jpg', [],
    ),

    # ── Salud y Bienestar ────────────────────────────────────────────────────
    (
        'Almohada de Masaje Car & Home 8028',
        'Salud y Bienestar',
        'Masaje profundo con nodos, terapia de calor e imanes. Para casa y auto.',
        'IMG-20260517-WA0090.jpg', [],
    ),
    (
        'Chaleco Corrector de Postura Molded Compression Vest',
        'Salud y Bienestar',
        'Mejora tu postura y rendimiento. Diseño cruzado, material transpirable y elástico.',
        'IMG-20260517-WA0091.jpg', [],
    ),
    (
        'Faja Reductora Waist Training Corset',
        'Salud y Bienestar',
        'Reduce cintura, aumenta sudoración y mejora la postura. Tecnología sauna effect.',
        'IMG-20260517-WA0092.jpg', [],
    ),
    (
        'Báscula Inteligente Healthy Weight Scale 180kg',
        'Salud y Bienestar',
        'Mide peso, grasa, músculo, IMC y más. App Bluetooth, vidrio templado, hasta 180 kg.',
        'IMG-20260517-WA0097.jpg', ['IMG-20260517-WA0125.jpg'],
    ),
    (
        'Almohada de Masaje para Cuello en U con Calor',
        'Salud y Bienestar',
        '4 nodos masajeadores con calor para cuello y hombros. Intensidad ajustable, suave y cómoda.',
        'IMG-20260517-WA0110.jpg', [],
    ),
    (
        'Gorro Alivio de Migraña Headache Relief Hat',
        'Salud y Bienestar',
        'Alivia migrañas y dolores de cabeza. Bloquea la luz, uso frío o tibio, reutilizable.',
        'IMG-20260517-WA0111.jpg', [],
    ),
    (
        'Entrenador de Piso Pélvico Pelvic Floor Muscle Trainer',
        'Salud y Bienestar',
        'Tonifica y fortalece el piso pélvico en casa. Silicona segura, pantalla digital, USB.',
        'IMG-20260517-WA0104.jpg', [],
    ),
    (
        'Faja Reductora Hot Shapers Unisex Neotex',
        'Salud y Bienestar',
        'Para hombre y mujer. Tecnología Neotex aumenta sudoración, reduce abdomen y cintura.',
        'IMG-20260517-WA0129.jpg', [],
    ),
    (
        'Masajeador Inteligente para la Cabeza',
        'Salud y Bienestar',
        'Alivia el estrés, mejora el sueño y la circulación. Ajustable, recargable USB.',
        'IMG-20260517-WA0142.jpg', [],
    ),
    (
        'Cojín Ergonómico para Caderas Longrong',
        'Salud y Bienestar',
        'Espuma viscoelástica para oficina, auto y hogar. Alivia caderas, espalda y cóccix.',
        'IMG-20260517-WA0143.jpg', [],
    ),
    (
        'Kit Dental de Viaje Teeth Cleaning Kit',
        'Salud y Bienestar',
        'Incluye cepillo, pasta dental, vaso y limpia lenguas. Diseño hermético portátil.',
        'IMG-20260517-WA0081.jpg', [],
    ),
    (
        'Cepillo Dental con Dispensador de Crema Dental',
        'Salud y Bienestar',
        'Dispensador integrado para viajes. Diseño compacto, higiénico y elegante, 2 colores.',
        'IMG-20260517-WA0139.jpg', [],
    ),
    (
        'Portacepillos con Esterilizador UV Solar',
        'Salud y Bienestar',
        'Esteriliza el 99.9% de bacterias con luz UV. Energía solar, sin cables, adhesivo para pared.',
        'IMG-20260517-WA0130.jpg', [],
    ),

    # ── Belleza y Cuidado Personal ───────────────────────────────────────────
    (
        'Máquina Corta Pelo Profesional 9 Piezas (Con Cable)',
        'Belleza y Cuidado Personal',
        'Motor potente, cuchillas de acero inoxidable. Kit completo con peines y accesorios.',
        'IMG-20260517-WA0088.jpg', [],
    ),
    (
        'DermaWand Pro – Dispositivo Antiedad Facial',
        'Belleza y Cuidado Personal',
        'Reduce arrugas y líneas finas. Estimula colágeno, mejora elasticidad, tecnología no invasiva.',
        'IMG-20260517-WA0115.jpg', [],
    ),
    (
        'Dispositivo de Alta Frecuencia Portátil ZL-006A',
        'Belleza y Cuidado Personal',
        'Mejora el acné, reduce poros y arrugas. Tecnología de alta frecuencia para uso doméstico.',
        'IMG-20260517-WA0118.jpg', [],
    ),
    (
        'Cortadora Alstow NS-308 – 3 en 1 Barba y Cabello',
        'Belleza y Cuidado Personal',
        'Barbear, afeitar y rasurar en uno. Cuchilla ultra delgada, 80 min de uso continuo.',
        'IMG-20260517-WA0120.jpg', [],
    ),
    (
        'Kit de Belleza Recargable Geemy GM-3074 – 4 en 1',
        'Belleza y Cuidado Personal',
        'Cabezal nariz, recortador cejas, afeitadora facial y corporal. Uso seco y húmedo.',
        'IMG-20260517-WA0131.jpg', [],
    ),
    (
        'Cortadora de Pelo Kemei KM-2900 Profesional',
        'Belleza y Cuidado Personal',
        'Cuchillas acero inoxidable, 120 min de batería. 4 peines guía intercambiables.',
        'IMG-20260517-WA0134.jpg', [],
    ),

    # ── Deportes y Fitness ───────────────────────────────────────────────────
    (
        'Toalla de Enfriamiento – 5 Colores',
        'Deportes y Fitness',
        'Enfría al instante al contacto con agua. Secado ultrarrápido, ideal para entrenamientos.',
        'IMG-20260517-WA0095.jpg', [],
    ),
    (
        'Banda Deportiva Trasera Ajustable Sports',
        'Deportes y Fitness',
        'Mantiene el sudor y cabello fuera del rostro. Antideslizante, ajustable, morada o negra.',
        'IMG-20260517-WA0105.jpg', [],
    ),
    (
        'Pedal Exerciser – Bicicleta de Escritorio',
        'Deportes y Fitness',
        'Ejercita brazos y piernas desde casa o la oficina. Resistencia ajustable, pantalla multifunción.',
        'IMG-20260517-WA0108.jpg', [],
    ),
    (
        'Bandas de Resistencia Hip Tela – 3 Niveles',
        'Deportes y Fitness',
        'Tela antideslizante premium para glúteos y piernas. 3 niveles de resistencia, bolsa incluida.',
        'IMG-20260517-WA0148.jpg', ['IMG-20260517-WA0149.jpg'],
    ),
    (
        'Bandas de Resistencia Látex – 5 Niveles',
        'Deportes y Fitness',
        'Set de 5 bandas multicolor en látex. Para piernas, glúteos y brazos, fáciles de transportar.',
        'IMG-20260517-WA0150.jpg', [],
    ),
    (
        'Rueda Abdominal con Rebote Automático y Timer',
        'Deportes y Fitness',
        'Fortalece el core con rebote automático. Incluye timer digital y apoyapiés acolchados.',
        'IMG-20260517-WA0156.jpg', [],
    ),

    # ── Hogar y Organización ─────────────────────────────────────────────────
    (
        'Llavero con Luz LED Estilo Auto Trueno',
        'Hogar y Organización',
        'Luces LED que se encienden al colgar las llaves. Imán fuerte, fácil instalación sin taladro.',
        'IMG-20260517-WA0077.jpg', [],
    ),
    (
        'Inflador Eléctrico para Globos – Doble Boquilla',
        'Hogar y Organización',
        'Infla cientos de globos en minutos con doble boquilla. Silencioso, portátil y seguro.',
        'IMG-20260517-WA0086.jpg', ['IMG-20260517-WA0155.jpg'],
    ),
    (
        'Toalla Magnética para Privacidad',
        'Hogar y Organización',
        'Imanes en cada esquina para adherirse a la puerta del carro. Ideal para cambiarse al aire libre.',
        'IMG-20260517-WA0093.jpg', [],
    ),
    (
        'Esquinero de Baño Metálico Negro',
        'Hogar y Organización',
        'Metal anticorrosivo de alta calidad. Instalación sin herramientas, adhesivo de alta adherencia.',
        'IMG-20260517-WA0101.jpg', ['IMG-20260517-WA0102.jpg'],
    ),
    (
        'Termo Inteligente Smart Cup con Pantalla LED',
        'Hogar y Organización',
        'Muestra la temperatura en tiempo real. Acero inoxidable, frío 12h / caliente 8h. 5 colores.',
        'IMG-20260517-WA0106.jpg', [],
    ),
    (
        'Cesta Plegable para Ropa Sucia – 3 Compartimentos',
        'Hogar y Organización',
        'Estructura metálica resistente, material impermeable. Plegable para ahorrar espacio.',
        'IMG-20260517-WA0117.jpg', ['IMG-20260517-WA0127.jpg'],
    ),
    (
        'Zapatero Compacto de 4 Niveles',
        'Hogar y Organización',
        'Ordena hasta 8 pares de zapatos. Diseño compacto, resistente y fácil de armar.',
        'IMG-20260517-WA0128.jpg', [],
    ),
    (
        'Secador de Zapatos Eléctrico Shoe Dryer',
        'Hogar y Organización',
        'Circulación de aire 360° a 48°C. Elimina humedad, hongos y malos olores. Temporizador 30–120 min.',
        'IMG-20260517-WA0138.jpg', [],
    ),
    (
        'Secadora Eléctrica Portátil para Ropa Drying Heater',
        'Hogar y Organización',
        'Seca ropa en minutos. Temporizador inteligente, bajo consumo de energía, 2 colores.',
        'IMG-20260517-WA0154.jpg', [],
    ),
    (
        'Set Termo Premium Vacuum Flask con 2 Tazas',
        'Hogar y Organización',
        'Termo + 2 tazas de acero inoxidable 304, frío/caliente 12 horas. Incluye caja regalo.',
        'IMG-20260517-WA0168.jpg', [],
    ),
    (
        'Kit de Limpieza para Zapatos Poetry Health',
        'Hogar y Organización',
        'Limpia, protege e impermeabiliza todo tipo de materiales. Incluye cepillos, esponja y spray.',
        'IMG-20260517-WA0164.jpg', [],
    ),
    (
        'Bolsa de Lavado para Zapatos',
        'Hogar y Organización',
        'Protege tus zapatos en la lavadora. Malla transpirable, cierre resistente, reutilizable.',
        'IMG-20260517-WA0166.jpg', [],
    ),

    # ── Herramientas y Vehículos ─────────────────────────────────────────────
    (
        'Inflador Portátil para Llantas con Pantalla Digital',
        'Herramientas y Vehículos',
        'Inflado rápido en 30 segundos. Pantalla LED, batería recargable, luz LED incorporada.',
        'IMG-20260517-WA0078.jpg', [],
    ),
    (
        'Martillo con Imán Oudisi 13oz',
        'Herramientas y Vehículos',
        'Sujeta clavos y puntas con el imán integrado. Material resistente y de alta calidad.',
        'IMG-20260517-WA0094.jpg', [],
    ),
    (
        'Kit Taladro Inalámbrico Boashi 21V',
        'Herramientas y Vehículos',
        'Motor potente, 17 posiciones de torque, luz LED. Kit completo con 2 baterías y maleta.',
        'IMG-20260517-WA0098.jpg', [],
    ),
    (
        'Mini Pulidora Inalámbrica 12V',
        'Herramientas y Vehículos',
        'Cortes y pulidos en metal, cerámica, madera y plástico. Kit completo con maleta y 2 baterías.',
        'IMG-20260517-WA0099.jpg', [],
    ),
    (
        'Pistola de Agua Multiusos para Vehículos y Jardín',
        'Herramientas y Vehículos',
        'Chorro ajustable, conectores metálicos anticorrosión. Para autos, motos, jardines y más.',
        'IMG-20260517-WA0100.jpg', [],
    ),
    (
        'Kit Taladro Inalámbrico Boashi 24V',
        'Herramientas y Vehículos',
        'Taladro inalámbrico 24V con 2 baterías litio. Accesorios completos, luz LED integrada.',
        'IMG-20260517-WA0112.jpg', [],
    ),
    (
        'Kit de Destornilladores de Precisión HRM07',
        'Herramientas y Vehículos',
        'Puntas magnéticas, organizador compacto. Ideal para celulares, laptops, relojes y gafas.',
        'IMG-20260517-WA0116.jpg', [],
    ),
    (
        'Ducha Portátil para Camping y Mascotas',
        'Herramientas y Vehículos',
        'Batería recargable USB, flujo de agua constante. Para mascotas, auto, camping y playa.',
        'IMG-20260517-WA0144.jpg', [],
    ),
    (
        'Arrancador Portátil de Vehículos con Inflador',
        'Herramientas y Vehículos',
        'Arranca tu vehículo en segundos. Incluye inflador de llantas, cables inteligentes y cargador.',
        'IMG-20260517-WA0145.jpg', [],
    ),
    (
        'Pulidor Inalámbrico Compacto para Auto',
        'Herramientas y Vehículos',
        'Brillo profesional inalámbrico y recargable. Para pintura, faros, vidrios y rines.',
        'IMG-20260517-WA0158.jpg', ['IMG-20260517-WA0159.jpg'],
    ),
    (
        'Kit Taladro Inalámbrico Amarillo con Maleta',
        'Herramientas y Vehículos',
        'Taladro inalámbrico potente con 2 baterías. Luz LED, torque ajustable y maletín resistente.',
        'IMG-20260517-WA0160.jpg', [],
    ),
    (
        'Pistola Eléctrica para Pintar Electric Sprayer Elite',
        'Herramientas y Vehículos',
        '3 patrones de rociado. Para paredes, muebles, puertas y más. Motor de alto rendimiento.',
        'IMG-20260517-WA0161.jpg', [],
    ),
    (
        'Set de Lavado para Vehículos con Cepillo Jabonero',
        'Herramientas y Vehículos',
        'Cepillo con jabonera integrada y mango extensible. Limpieza profunda para auto y moto.',
        'IMG-20260517-WA0157.jpg', [],
    ),
    (
        'Auricular Inalámbrico para Casco de Moto Wireless Earphone',
        'Herramientas y Vehículos',
        'Llamadas automáticas y música mientras conduces. Bluetooth, compatible con GPS, resistente al agua.',
        'IMG-20260517-WA0167.jpg', [],
    ),
    (
        'Candado de Disco con Alarma para Moto U-Know',
        'Herramientas y Vehículos',
        'Alarma de alta sensibilidad ante intentos de robo. Resistente al agua, batería de larga duración.',
        'IMG-20260517-WA0170.jpg', [],
    ),

    # ── Mascotas ─────────────────────────────────────────────────────────────
    (
        'Correa Doble Retráctil para 2 Perros con Luz LED',
        'Mascotas',
        'Sin enredos, con linterna LED y dispensador de bolsas. Cintas retráctiles 360°.',
        'IMG-20260517-WA0096.jpg', [],
    ),
    (
        'Cobertor de Sofá Reversible para Mascotas',
        'Mascotas',
        'Protege el sofá de mascotas, derrames y manchas. Lavable a máquina, reversible.',
        'IMG-20260517-WA0126.jpg', [],
    ),
    (
        'Cepillo Masajeador Eléctrico con Spray para Mascotas',
        'Mascotas',
        'Spray integrado para hidratar. Elimina pelo suelto, masajea y mejora la circulación.',
        'IMG-20260517-WA0119.jpg', [],
    ),
    (
        'Comedero Doble Automático con Temporizador para Mascotas',
        'Mascotas',
        'Programa hasta 48 horas por adelantado. Doble bandeja, libre de BPA, fácil de limpiar.',
        'IMG-20260517-WA0133.jpg', [],
    ),

    # ── Bebé y Maternidad ────────────────────────────────────────────────────
    (
        'Cepillo Eléctrico para Biberones con Esterilizador UV',
        'Bebé y Maternidad',
        'Limpieza profunda y esterilización UV que elimina el 99.9% de bacterias. Silicona libre de BPA.',
        'IMG-20260517-WA0103.jpg', [],
    ),
    (
        'Extractor de Leche Eléctrico Doble MZ-608T',
        'Bebé y Maternidad',
        'Extracción cómoda y silenciosa. Libre de BPA, recargable USB, suave y eficiente.',
        'IMG-20260517-WA0114.jpg', [],
    ),

    # ── Juguetes y Entretenimiento ───────────────────────────────────────────
    (
        'Kit Spray Pen para Niños Hobby & Fun',
        'Juguetes y Entretenimiento',
        'Spray pen recargable con 8 plumones y 4 plantillas. Seguro, no tóxico, estimula la creatividad.',
        'IMG-20260517-WA0080.jpg', [],
    ),
    (
        'Consola Game Box KR-J9 – 500 Juegos Clásicos',
        'Juguetes y Entretenimiento',
        'Pantalla a color, batería recargable, compacta y portátil. Varios diseños disponibles.',
        'IMG-20260517-WA0107.jpg', [],
    ),
    (
        'Kids Walkie-Talkies Diseño Conejito',
        'Juguetes y Entretenimiento',
        'Alcance hasta 3 km. Pantalla LCD, linterna integrada, clip para cinturón. Para mayores de 6 años.',
        'IMG-20260517-WA0121.jpg', ['IMG-20260517-WA0122.jpg'],
    ),
]


def img_to_b64(filename):
    path = os.path.join(IMGS_DIR, filename)
    if not os.path.exists(path):
        return None
    ext = filename.rsplit('.', 1)[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else 'image/png'
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f'data:{mime};base64,{data}'


class Command(BaseCommand):
    help = 'Carga el catálogo completo de productos con imágenes desde /tmp/catalogo_imgs2/Catalogoso'

    def handle(self, *args, **options):
        # Crear categorías
        cats = {}
        for nombre, orden in CATEGORIAS:
            cat, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'orden': orden},
            )
            if not created:
                cat.orden = orden
                cat.save()
            cats[nombre] = cat
            self.stdout.write(f'  {"Creada" if created else "Existente"} categoría: {nombre}')

        self.stdout.write(self.style.SUCCESS(f'\n{len(CATEGORIAS)} categorías listas.\n'))

        creados = 0
        omitidos = 0
        sin_imagen = 0

        for nombre, cat_nombre, desc_corta, img_principal, imgs_extra in PRODUCTOS:
            if Producto.objects.filter(nombre=nombre).exists():
                self.stdout.write(f'  Omitido (ya existe): {nombre}')
                omitidos += 1
                continue

            b64_principal = img_to_b64(img_principal)
            if b64_principal is None:
                self.stdout.write(
                    self.style.WARNING(f'  Sin imagen principal ({img_principal}): {nombre}')
                )
                sin_imagen += 1

            producto = Producto.objects.create(
                nombre=nombre,
                categoria=cats[cat_nombre],
                descripcion_corta=desc_corta,
                imagen_data=b64_principal or '',
                disponible=True,
            )

            for i, extra_fn in enumerate(imgs_extra):
                b64_extra = img_to_b64(extra_fn)
                if b64_extra:
                    ProductoImagen.objects.create(
                        producto=producto,
                        imagen_data=b64_extra,
                        orden=i,
                    )

            self.stdout.write(
                f'  ✓ {nombre} '
                f'[{1 + len(imgs_extra)} imagen(es)]'
            )
            creados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nListo: {creados} productos creados, '
                f'{omitidos} omitidos, '
                f'{sin_imagen} sin imagen principal.'
            )
        )
