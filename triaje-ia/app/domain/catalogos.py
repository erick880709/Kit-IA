"""Catálogos de dominio (RD-002, HU-E2-01).

- DEPARTAMENTOS_COLOMBIA: 32 departamentos.
- CIUDADES_POR_DEPARTAMENTO: TODOS los municipios oficiales por departamento
  (DANE) — reemplaza el subconjunto demo anterior.
- EPS_COLOMBIA: EPS/IPS habilitadas (régimen contributivo y subsidiado).
- VIA_LLEGADA: catálogo exigido por HU-E2-01 CA1.
- SEXO: catálogo demográfico.
"""

from __future__ import annotations

DEPARTAMENTOS_COLOMBIA: list[str] = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá",
    "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba",
    "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira",
    "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo",
    "Quindío", "Risaralda", "San Andrés y Providencia", "Santander",
    "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada",
]

CIUDADES_POR_DEPARTAMENTO: dict[str, list[str]] = {
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": [
        "Medellín", "Abejorral", "Abriaquí", "Alejandría", "Amagá", "Amalfi",
        "Andes", "Angelópolis", "Angostura", "Anorí", "Anzá", "Apartadó",
        "Arboletes", "Argelia", "Barbosa", "Bello", "Belmira", "Betania",
        "Betulia", "Briceño", "Buriticá", "Cáceres", "Caicedo", "Caldas",
        "Campamento", "Cañasgordas", "Caracolí", "Caramanta", "Carepa",
        "Carolina del Príncipe", "Caucasia", "Chigorodó", "Cisneros",
        "Ciudad Bolívar", "Cocorná", "Concepción", "Concordia", "Copacabana",
        "Dabeiba", "Donmatías", "Ebéjico", "El Bagre", "El Carmen de Viboral",
        "El Peñol", "El Retiro", "El Santuario", "Entrerríos", "Envigado",
        "Fredonia", "Frontino", "Giraldo", "Girardota", "Gómez Plata",
        "Granada", "Guadalupe", "Guarne", "Guatapé", "Heliconia", "Hispania",
        "Itagüí", "Ituango", "Jardín", "Jericó", "La Ceja", "La Estrella",
        "La Pintada", "La Unión", "Liborina", "Maceo", "Marinilla",
        "Montebello", "Murindó", "Mutatá", "Nariño", "Nechí", "Necoclí",
        "Olaya", "Peque", "Pueblorrico", "Puerto Berrío", "Puerto Nare",
        "Puerto Triunfo", "Remedios", "Rionegro", "Sabanalarga", "Sabaneta",
        "Salgar", "San Andrés de Cuerquia", "San Carlos", "San Francisco",
        "San Jerónimo", "San José de la Montaña", "San Juan de Urabá",
        "San Luis", "San Pedro de los Milagros", "San Pedro de Urabá",
        "San Rafael", "San Roque", "San Vicente Ferrer", "Santa Bárbara",
        "Santa Fe de Antioquia", "Santa Rosa de Osos", "Santo Domingo",
        "Segovia", "Sonsón", "Sopetrán", "Támesis", "Tarazá", "Tarso",
        "Titiribí", "Toledo", "Turbo", "Uramita", "Urrao", "Valdivia",
        "Valparaíso", "Vegachí", "Venecia", "Vigía del Fuerte", "Yalí",
        "Yarumal", "Yolombó", "Yondó", "Zaragoza",
    ],
    "Arauca": [
        "Arauca", "Arauquita", "Cravo Norte", "Fortul", "Puerto Rondón",
        "Saravena", "Tame",
    ],
    "Atlántico": [
        "Barranquilla", "Baranoa", "Campo de la Cruz", "Candelaria", "Galapa",
        "Juan de Acosta", "Luruaco", "Malambo", "Manatí", "Palmar de Varela",
        "Piojó", "Polonuevo", "Ponedera", "Puerto Colombia", "Repelón",
        "Sabanagrande", "Sabanalarga", "Santa Lucía", "Santo Tomás", "Soledad",
        "Suan", "Tubará", "Usiacurí",
    ],
    "Bolívar": [
        "Cartagena de Indias", "Achí", "Altos del Rosario", "Arenal", "Arjona",
        "Arroyohondo", "Barranco de Loba", "Calamar", "Cantagallo", "Cicuco",
        "Clemencia", "Córdoba", "El Carmen de Bolívar", "El Guamo", "El Peñón",
        "Hatillo de Loba", "Magangué", "Mahates", "Margarita", "María la Baja",
        "Montecristo", "Morales", "Norosí", "Pinillos", "Regidor", "Río Viejo",
        "San Cristóbal", "San Estanislao", "San Fernando", "San Jacinto",
        "San Jacinto del Cauca", "San Juan Nepomuceno", "San Martín de Loba",
        "San Pablo", "Santa Catalina", "Santa Rosa", "Santa Rosa del Sur",
        "Simití", "Soplaviento", "Talaigua Nuevo", "Tiquisio", "Turbaco",
        "Turbaná", "Villanueva", "Zambrano",
    ],
    "Boyacá": [
        "Tunja", "Almeida", "Aquitania", "Arcabuco", "Belén", "Berbeo",
        "Betéitiva", "Boavita", "Boyacá", "Briceño", "Buenavista", "Busbanzá",
        "Caldas", "Campohermoso", "Cerinza", "Chinavita", "Chiquinquirá",
        "Chíquiza", "Chiscas", "Chita", "Chitaraque", "Chivatá", "Ciénega",
        "Cómbita", "Coper", "Corrales", "Covarachía", "Cubará", "Cucaita",
        "Cuítiva", "Duitama", "El Cocuy", "El Espino", "Firavitoba", "Floresta",
        "Gachantivá", "Gámeza", "Garagoa", "Guacamayas", "Guateque", "Guayatá",
        "Güicán de la Sierra", "Iza", "Jenesano", "Jericó", "La Capilla",
        "La Uvita", "La Victoria", "Labranzagrande", "Macanal", "Maripí",
        "Miraflores", "Mongua", "Monguí", "Moniquirá", "Motavita", "Muzo",
        "Nobsa", "Nuevo Colón", "Oicatá", "Otanche", "Pachavita", "Páez",
        "Paipa", "Pajarito", "Panqueba", "Pauna", "Paya", "Paz de Río",
        "Pesca", "Pisba", "Puerto Boyacá", "Quípama", "Ramiriquí", "Ráquira",
        "Rondón", "Saboyá", "Sáchica", "Samacá", "San Eduardo",
        "San José de Pare", "San Luis de Gaceno", "San Mateo",
        "San Miguel de Sema", "San Pablo de Borbur", "Santa María",
        "Santa Rosa de Viterbo", "Santa Sofía", "Santana", "Sativanorte",
        "Sativasur", "Siachoque", "Soatá", "Socha", "Socotá", "Sogamoso",
        "Somondoco", "Sora", "Soracá", "Sotaquirá", "Susacón", "Sutamarchán",
        "Sutatenza", "Tasco", "Tenza", "Tibaná", "Tibasosa", "Tinjacá",
        "Tipacoque", "Toca", "Togüí", "Tópaga", "Tota", "Tununguá",
        "Turmequé", "Tuta", "Tutazá", "Úmbita", "Ventaquemada", "Villa de Leyva",
        "Viracachá", "Zetaquira",
    ],
    "Caldas": [
        "Manizales", "Aguadas", "Anserma", "Aranzazu", "Belalcázar", "Chinchiná",
        "Filadelfia", "La Dorada", "La Merced", "Manzanares", "Marmato",
        "Marquetalia", "Marulanda", "Neira", "Norcasia", "Pácora", "Palestina",
        "Pensilvania", "Riosucio", "Risaralda", "Salamina", "Samaná", "Supía",
        "Victoria", "Villamaría", "Viterbo",
    ],
    "Caquetá": [
        "Florencia", "Albania", "Belén de los Andaquíes", "Cartagena del Chairá",
        "Curillo", "El Doncello", "El Paujil", "La Montañita", "Milán",
        "Morelia", "Puerto Rico", "San José del Fragua", "San Vicente del Caguán",
        "Solano", "Solita", "Valparaíso",
    ],
    "Casanare": [
        "Yopal", "Aguazul", "Chámeza", "Hato Corozal", "La Salina", "Maní",
        "Monterrey", "Nunchía", "Orocué", "Paz de Ariporo", "Pore", "Recetor",
        "Sabanalarga", "Sácama", "San Luis de Palenque", "Támara", "Tauramena",
        "Trinidad", "Villanueva",
    ],
    "Cauca": [
        "Popayán", "Almaguer", "Argelia", "Balboa", "Bolívar", "Buenos Aires",
        "Cajibío", "Caldono", "Caloto", "Corinto", "El Tambo", "Florencia",
        "Guachené", "Guapi", "Inzá", "Jambaló", "La Sierra", "La Vega",
        "López de Micay", "Mercaderes", "Miranda", "Morales", "Padilla",
        "Páez", "Patía", "Piamonte", "Piendamó", "Puerto Tejada", "Puracé",
        "Rosas", "San Sebastián", "Santander de Quilichao", "Santa Rosa",
        "Silvia", "Sotará", "Suárez", "Sucre", "Timbío", "Timbiquí",
        "Toribío", "Totoró", "Villa Rica",
    ],
    "Cesar": [
        "Valledupar", "Aguachica", "Agustín Codazzi", "Astrea", "Becerril",
        "Bosconia", "Chimichagua", "Chiriguaná", "Curumaní", "El Copey",
        "El Paso", "Gamarra", "González", "La Gloria", "La Jagua de Ibirico",
        "La Paz", "Manaure Balcón del Cesar", "Pailitas", "Pelaya",
        "Pueblo Bello", "Río de Oro", "San Alberto", "San Diego", "San Martín",
        "Tamalameque",
    ],
    "Chocó": [
        "Quibdó", "Acandí", "Alto Baudó", "Atrato", "Bagadó", "Bahía Solano",
        "Bajo Baudó", "Bojayá", "Carmen del Darién", "Cértegui", "Condoto",
        "El Cantón del San Pablo", "El Carmen de Atrato", "El Litoral del San Juan",
        "Istmina", "Juradó", "Lloró", "Medio Atrato", "Medio Baudó",
        "Medio San Juan", "Nóvita", "Nuquí", "Río Iró", "Río Quito", "Riosucio",
        "San José del Palmar", "Sipí", "Tadó", "Unguía", "Unión Panamericana",
    ],
    "Córdoba": [
        "Montería", "Ayapel", "Buenavista", "Canalete", "Cereté", "Chimá",
        "Chinú", "Ciénaga de Oro", "Cotorra", "La Apartada", "Lorica",
        "Los Córdobas", "Momil", "Montelíbano", "Moñitos", "Planeta Rica",
        "Pueblo Nuevo", "Puerto Escondido", "Puerto Libertador",
        "Purísima de la Concepción", "Sahagún", "San Andrés de Sotavento",
        "San Antero", "San Bernardo del Viento", "San Carlos", "San José de Uré",
        "San Pelayo", "Tierralta", "Tuchín", "Valencia",
    ],
    "Cundinamarca": [
        "Bogotá D.C.", "Agua de Dios", "Albán", "Anapoima", "Anolaima",
        "Apulo", "Arbeláez", "Beltrán", "Bituima", "Bojacá", "Cabrera",
        "Cachipay", "Cajicá", "Caparrapí", "Cáqueza", "Carmen de Carupa",
        "Chaguaní", "Chía", "Chipaque", "Choachí", "Chocontá", "Cogua",
        "Cota", "Cucunubá", "El Colegio", "El Peñón", "El Rosal", "Facatativá",
        "Fómeque", "Fosca", "Funza", "Fúquene", "Fusagasugá", "Gachalá",
        "Gachancipá", "Gachetá", "Gama", "Girardot", "Granada", "Guachetá",
        "Guaduas", "Guasca", "Guataquí", "Guatavita", "Guayabal de Síquima",
        "Guayabetal", "Gutiérrez", "Jerusalén", "Junín", "La Calera",
        "La Mesa", "La Palma", "La Peña", "La Vega", "Lenguazaque", "Machetá",
        "Madrid", "Manta", "Medina", "Mosquera", "Nariño", "Nemocón", "Nilo",
        "Nimaima", "Nocaima", "Pacho", "Paime", "Pandi", "Paratebueno",
        "Pasca", "Puerto Salgar", "Pulí", "Quebradanegra", "Quetame", "Quipile",
        "Ricaurte", "San Antonio del Tequendama", "San Bernardo", "San Cayetano",
        "San Francisco", "San Juan de Rioseco", "Sasaima", "Sesquilé", "Sibaté",
        "Silvania", "Simijaca", "Soacha", "Sopó", "Subachoque", "Suesca",
        "Supatá", "Susa", "Sutatausa", "Tabio", "Tausa", "Tena", "Tenjo",
        "Tibacuy", "Tibirita", "Tocaima", "Tocancipá", "Topaipí", "Ubalá",
        "Ubaque", "Ubaté", "Une", "Útica", "Venecia", "Vergara", "Vianí",
        "Villagómez", "Villapinzón", "Villeta", "Viotá", "Yacopí", "Zipacón",
        "Zipaquirá",
    ],
    "Guainía": [
        "Inírida", "Barranco Minas", "Cacahual", "La Guadalupe", "Mapiripana",
        "Morichal", "Pana Pana", "Puerto Colombia", "San Felipe",
    ],
    "Guaviare": [
        "San José del Guaviare", "Calamar", "El Retorno", "Miraflores",
    ],
    "Huila": [
        "Neiva", "Acevedo", "Agrado", "Aipe", "Algeciras", "Altamira", "Baraya",
        "Campoalegre", "Colombia", "Elías", "Garzón", "Gigante", "Guadalupe",
        "Hobo", "Íquira", "Isnos", "La Argentina", "La Plata", "Nátaga",
        "Oporapa", "Paicol", "Palermo", "Palestina", "Pital", "Pitalito",
        "Rivera", "Saladoblanco", "San Agustín", "Santa María", "Suaza",
        "Tarqui", "Tello", "Teruel", "Tesalia", "Timaná", "Villavieja",
        "Yaguará",
    ],
    "La Guajira": [
        "Riohacha", "Albania", "Barrancas", "Dibulla", "Distracción",
        "El Molino", "Fonseca", "Hatonuevo", "La Jagua del Pilar", "Maicao",
        "Manaure", "San Juan del Cesar", "Uribia", "Urumita", "Villanueva",
    ],
    "Magdalena": [
        "Santa Marta", "Algarrobo", "Aracataca", "Ariguaní", "Cerro de San Antonio",
        "Chivolo", "Ciénaga", "Concordia", "El Banco", "El Piñón", "El Retén",
        "Fundación", "Guamal", "Nueva Granada", "Pedraza", "Pijiño del Carmen",
        "Pivijay", "Plato", "Puebloviejo", "Remolino", "Sabanas de San Ángel",
        "Salamina", "San Sebastián de Buenavista", "San Zenón", "Santa Ana",
        "Santa Bárbara de Pinto", "Sitionuevo", "Tenerife", "Zapayán",
        "Zona Bananera",
    ],
    "Meta": [
        "Villavicencio", "Acacías", "Barranca de Upía", "Cabuyaro",
        "Castilla la Nueva", "Cubarral", "Cumaral", "El Calvario", "El Castillo",
        "El Dorado", "Fuente de Oro", "Granada", "Guamal", "La Macarena",
        "La Uribe", "Lejanías", "Mapiripán", "Mesetas", "Puerto Concordia",
        "Puerto Gaitán", "Puerto Lleras", "Puerto López", "Puerto Rico",
        "Restrepo", "San Carlos de Guaroa", "San Juan de Arama", "San Juanito",
        "San Martín", "Vista Hermosa",
    ],
    "Nariño": [
        "Pasto", "Albán", "Aldana", "Ancuyá", "Arboleda", "Barbacoas", "Belén",
        "Buesaco", "Chachagüí", "Colón", "Consacá", "Contadero", "Córdoba",
        "Cuaspud", "Cumbal", "Cumbitara", "El Charco", "El Peñol", "El Rosario",
        "El Tablón de Gómez", "El Tambo", "Francisco Pizarro", "Funes",
        "Guachucal", "Guaitarilla", "Gualmatán", "Iles", "Imués", "Ipiales",
        "La Cruz", "La Florida", "La Llanada", "La Tola", "La Unión", "Leiva",
        "Linares", "Los Andes", "Magüí Payán", "Mallama", "Mosquera", "Nariño",
        "Olaya Herrera", "Ospina", "Policarpa", "Potosí", "Providencia",
        "Puerres", "Pupiales", "Ricaurte", "Roberto Payán", "Samaniego",
        "San Bernardo", "San Lorenzo", "San Pablo", "San Pedro de Cartago",
        "Sandoná", "Santa Bárbara", "Santacruz", "Sapuyes", "Taminango",
        "Tangua", "Tumaco", "Túquerres", "Yacuanquer",
    ],
    "Norte de Santander": [
        "Cúcuta", "Abrego", "Arboledas", "Bochalema", "Bucarasica", "Cáchira",
        "Cácota", "Chinácota", "Chitagá", "Convención", "Cucutilla", "Durania",
        "El Carmen", "El Tarra", "El Zulia", "Gramalote", "Hacarí", "Herrán",
        "La Esperanza", "La Playa de Belén", "Labateca", "Los Patios", "Lourdes",
        "Mutiscua", "Ocaña", "Pamplona", "Pamplonita", "Puerto Santander",
        "Ragonvalia", "Salazar de las Palmas", "San Calixto", "San Cayetano",
        "Santiago", "Sardinata", "Silos", "Teorama", "Tibú", "Toledo",
        "Villa Caro", "Villa del Rosario",
    ],
    "Putumayo": [
        "Mocoa", "Colón", "Orito", "Puerto Asís", "Puerto Caicedo",
        "Puerto Guzmán", "Puerto Leguízamo", "San Francisco", "San Miguel",
        "Santiago", "Sibundoy", "Valle del Guamuez", "Villagarzón",
    ],
    "Quindío": [
        "Armenia", "Buenavista", "Calarcá", "Circasia", "Córdoba", "Filandia",
        "Génova", "La Tebaida", "Montenegro", "Pijao", "Quimbaya", "Salento",
    ],
    "Risaralda": [
        "Pereira", "Apía", "Balboa", "Belén de Umbría", "Dosquebradas",
        "Guática", "La Celia", "La Virginia", "Marsella", "Mistrató",
        "Pueblo Rico", "Quinchía", "Santa Rosa de Cabal", "Santuario",
    ],
    "San Andrés y Providencia": ["San Andrés", "Providencia"],
    "Santander": [
        "Bucaramanga", "Aguada", "Albania", "Aratoca", "Barbosa", "Barichara",
        "Barrancabermeja", "Betulia", "Bolívar", "Cabrera", "California",
        "Capitanejo", "Carcasí", "Cepitá", "Cerrito", "Charalá", "Charta",
        "Chima", "Chipatá", "Cimitarra", "Concepción", "Confines",
        "Contratación", "Coromoro", "Curití", "El Carmen de Chucurí",
        "El Guacamayo", "El Peñón", "El Playón", "Encino", "Enciso", "Florián",
        "Floridablanca", "Galán", "Gámbita", "Girón", "Guaca", "Guadalupe",
        "Guapotá", "Guavatá", "Güepsa", "Hato", "Jesús María", "Jordán",
        "La Belleza", "La Paz", "Landázuri", "Lebrija", "Los Santos",
        "Macaravita", "Málaga", "Matanza", "Mogotes", "Molagavita", "Ocamonte",
        "Oiba", "Onzaga", "Palmar", "Palmas del Socorro", "Páramo",
        "Piedecuesta", "Pinchote", "Puente Nacional", "Puerto Parra",
        "Puerto Wilches", "Rionegro", "Sabana de Torres", "San Andrés",
        "San Benito", "San Gil", "San Joaquín", "San José de Miranda",
        "San Miguel", "San Vicente de Chucurí", "Santa Bárbara",
        "Santa Helena del Opón", "Simacota", "Socorro", "Suaita", "Sucre",
        "Suratá", "Tona", "Valle de San José", "Vélez", "Vetas", "Villanueva",
        "Zapatoca",
    ],
    "Sucre": [
        "Sincelejo", "Buenavista", "Caimito", "Chalán", "Colosó", "Corozal",
        "Coveñas", "El Roble", "Galeras", "Guaranda", "La Unión", "Los Palmitos",
        "Majagual", "Morroa", "Ovejas", "Palmito", "Sampués", "San Benito Abad",
        "San Juan de Betulia", "San Marcos", "San Onofre", "San Pedro", "Sincé",
        "Sucre", "Tolú", "Toluviejo",
    ],
    "Tolima": [
        "Ibagué", "Alpujarra", "Alvarado", "Ambalema", "Anzoátegui",
        "Armero-Guayabal", "Ataco", "Cajamarca", "Carmen de Apicalá",
        "Casabianca", "Chaparral", "Coello", "Coyaima", "Cunday", "Dolores",
        "Espinal", "Falan", "Flandes", "Fresno", "Guamo", "Herveo", "Honda",
        "Icononzo", "Lérida", "Líbano", "Mariquita", "Melgar", "Murillo",
        "Natagaima", "Ortega", "Palocabildo", "Piedras", "Planadas", "Prado",
        "Purificación", "Rioblanco", "Roncesvalles", "Rovira", "Saldaña",
        "San Antonio", "San Luis", "Santa Isabel", "Suárez", "Valle de San Juan",
        "Venadillo", "Villahermosa", "Villarrica",
    ],
    "Valle del Cauca": [
        "Cali", "Alcalá", "Andalucía", "Ansermanuevo", "Argelia", "Bolívar",
        "Buenaventura", "Buga", "Bugalagrande", "Caicedonia", "Calima",
        "Candelaria", "Cartago", "Dagua", "El Águila", "El Cairo", "El Cerrito",
        "El Dovio", "Florida", "Ginebra", "Guacarí", "Jamundí", "La Cumbre",
        "La Unión", "La Victoria", "Obando", "Palmira", "Pradera", "Restrepo",
        "Riofrío", "Roldanillo", "San Pedro", "Sevilla", "Toro", "Trujillo",
        "Tuluá", "Ulloa", "Versalles", "Vijes", "Yotoco", "Yumbo", "Zarzal",
    ],
    "Vaupés": ["Mitú", "Carurú", "Taraira"],
    "Vichada": [
        "Puerto Carreño", "Cumaribo", "La Primavera", "Santa Rosalía",
    ],
}

EPS_COLOMBIA: list[str] = [
    "Nueva EPS", "Salud Total", "EPS Sura", "Sanitas", "Compensar",
    "Famisanar", "Comfenalco Valle", "Coomeva", "Salud Bolívar", "SOS",
    "Mutual Ser", "Cajacopi", "Coosalud", "Capital Salud", "Savia Salud",
    "Asmet Salud", "Emssanar", "Mallamas", "Anas Wayuu", "Dusakawi",
    "Ecoopsos", "Ambuq", "Comfamiliar Huila", "Comfachocó", "Comfaoriente",
    "Salud Mía", "Aliansalud", "Comparta", "Convida", "Capresoca", "Saludvida",
]

VIA_LLEGADA: list[str] = ["Ambulancia", "Particular", "Remisión"]

SEXO: list[str] = ["Femenino", "Masculino", "Intersexual", "Prefiero no informar"]

GRUPOS_SANGUINEOS: list[str] = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Niveles de triaje Res. 5596/2015 (RD-001).
NIVELES_TRIaje: list[str] = ["I", "II", "III", "IV", "V"]

# Catálogo de motivos de urgencias: (código CIE-11, descripción, categoría).
# Ampliado desde el top-10 inicial (RD-002) con el catálogo clínico completo.
# Los códigos CIE-11 mapean el catálogo CIE-10 original para la demo académica;
# el mapeo debe validarse con un referente clínico antes de uso real.
CATALOGO_MOTIVOS: list[tuple[str, str, str]] = [
    # Digestivo
    ("DD30", "Dolor abdominal no especificado", "Digestivo"),
    ("ME05", "Estreñimiento", "Digestivo"),
    ("MD90", "Náuseas y vómitos", "Digestivo"),
    ("DB24.B", "Hemorragia gastrointestinal no especificada", "Digestivo"),
    ("DB10", "Apendicitis aguda no especificada", "Digestivo"),
    ("1A40", "Gastroenteritis de presunto origen infeccioso", "Digestivo"),
    ("MD81.3", "Abdomen agudo", "Digestivo"),
    ("DA42", "Gastritis no especificada", "Digestivo"),
    # Respiratorio
    ("CA00", "Rinofaringitis aguda (resfriado común)", "Respiratorio"),
    ("CA07", "Infección aguda de vías respiratorias superiores, no especificada", "Respiratorio"),
    ("CA42", "Bronquitis aguda no especificada", "Respiratorio"),
    ("CA23", "Asma, no especificada", "Respiratorio"),
    ("CA40", "Neumonía no especificada", "Respiratorio"),
    ("MD12", "Tos", "Respiratorio"),
    ("MD11", "Disnea", "Respiratorio"),
    ("CB41", "Insuficiencia respiratoria aguda", "Respiratorio"),
    # Neurológico
    ("8A8Z", "Cefalea", "Neurológico"),
    ("MB48", "Mareo y desvanecimiento", "Neurológico"),
    ("MG45", "Síncope y colapso", "Neurológico"),
    ("8A68", "Convulsiones, no especificadas", "Neurológico"),
    ("8A80", "Migraña, no especificada", "Neurológico"),
    ("NA0Z", "Traumatismo craneal no especificado", "Neurológico"),
    # Cardiovascular
    ("MD30", "Dolor torácico no especificado", "Cardiovascular"),
    ("BA00", "Hipertensión esencial (primaria)", "Cardiovascular"),
    ("MC81", "Taquicardia, no especificada", "Cardiovascular"),
    ("MC80", "Bradicardia, no especificada", "Cardiovascular"),
    # Musculoesquelético
    ("ME84.2", "Lumbago no especificado", "Musculoesquelético"),
    ("ND14", "Esguince de tobillo", "Musculoesquelético"),
    ("NC32", "Fractura de antebrazo, parte no especificada", "Musculoesquelético"),
    ("ND12", "Herida de muñeca y de la mano, no especificada", "Musculoesquelético"),
    ("ND9Z", "Herida abierta, región del cuerpo no especificada", "Musculoesquelético"),
    ("ND90", "Quemadura de región del cuerpo no especificada, grado no "
     "especificado", "Musculoesquelético"),
    # Trauma
    ("ND5Z", "Fractura de región no especificada", "Trauma"),
    ("NC52", "Fractura de muñeca y mano, no especificada", "Trauma"),
    ("NC72", "Fractura de fémur, no especificada", "Trauma"),
    ("NC92", "Fractura de pierna, no especificada", "Trauma"),
    ("NA07", "Traumatismo intracraneal no especificado (TEC)", "Trauma"),
    ("PA80", "Herida por arma de fuego, no especificada", "Trauma"),
    ("PA75", "Herida por arma cortopunzante (cuchillo/daga)", "Trauma"),
    ("ND13", "Luxación, esguince o torcedura de región no especificada", "Trauma"),
    ("ND0Z", "Traumatismos múltiples no especificados (politraumatismo)", "Trauma"),
    ("ND50", "Lesión por aplastamiento o amputación traumática", "Trauma"),
    ("PA50", "Mordedura o ataque de perro", "Trauma"),
    ("PA60", "Caída no especificada", "Trauma"),
    ("PB80", "Electrocución (descarga eléctrica)", "Trauma"),
    ("NF08", "Ahogamiento y sumersión no mortal", "Trauma"),
    # Genitourinario
    ("GC08", "Infección de vías urinarias", "Genitourinario"),
    ("MF56", "Cólico renal, no especificado", "Genitourinario"),
    ("MF50.7", "Disuria", "Genitourinario"),
    ("MF50.4", "Hematuria no especificada", "Genitourinario"),
    # Ginecológico/Obstétrico
    ("GA34.3", "Dismenorrea, no especificada", "Ginecológico/Obstétrico"),
    ("JA65", "Complicación relacionada con el embarazo, no "
     "especificada", "Ginecológico/Obstétrico"),
    # Piel/Alergia
    ("EF50", "Celulitis, no especificada", "Piel/Alergia"),
    ("ME65", "Erupción y otras erupciones cutáneas no especificadas", "Piel/Alergia"),
    ("EC90", "Prurito, no especificado", "Piel/Alergia"),
    ("4A80", "Alergia, no especificada", "Piel/Alergia"),
    ("EB00", "Urticaria no especificada", "Piel/Alergia"),
    # ORL/Oftalmológico
    ("CA09", "Faringitis aguda, no especificada", "ORL/Oftalmológico"),
    ("CA0A", "Amigdalitis aguda, no especificada", "ORL/Oftalmológico"),
    ("AB00", "Otitis media, no especificada", "ORL/Oftalmológico"),
    ("9A60", "Conjuntivitis, no especificada", "ORL/Oftalmológico"),
    # Salud mental
    ("6B00", "Trastorno de ansiedad, no especificado", "Salud mental"),
    ("MB24.3", "Inquietud y agitación", "Salud mental"),
    # Endocrino/Metabólico
    ("5A41", "Hipoglicemia no especificada", "Endocrino/Metabólico"),
    # Hematológico
    ("3A00", "Anemia no especificada", "Hematológico"),
    # Signos/Síntomas generales
    ("MG26", "Fiebre no especificada", "Signos/Síntomas generales"),
    ("5C70", "Deshidratación", "Signos/Síntomas generales"),
    ("MG22", "Malestar y fatiga", "Signos/Síntomas generales"),
    ("MG43.7", "Anorexia", "Signos/Síntomas generales"),
    ("MB20", "Desorientación, no especificada", "Signos/Síntomas generales"),
    ("1D9Z", "Infección viral no especificada", "Signos/Síntomas generales"),
]

NIVEL_CONCIENCIA: list[str] = [
    "Alerta",
    "Responde a voz",
    "Responde al dolor",
    "No responde",
]

# Máquina de estados del triaje (HU-E2-06 CA1) y transiciones válidas (CA2).
ESTADOS_TRIaje: list[str] = [
    "Registrado",
    "SignosVitales",
    "EvaluacionClinica",
    "ClasificacionIA",
    "ValidacionProfesional",
    "Cerrado",
    "Reclasificado",
]

TRANSICIONES_VALIDAS: dict[str, set[str]] = {
    # "Cerrado" directo desde "Registrado" solo lo produce el cierre automático
    # por menor de 16 años (sin recomendación IA, nivel a cargo del profesional).
    "Registrado": {"SignosVitales", "Cerrado"},
    "SignosVitales": {"EvaluacionClinica"},
    "EvaluacionClinica": {"ClasificacionIA"},
    "ClasificacionIA": {"ValidacionProfesional"},
    "ValidacionProfesional": {"Cerrado"},
    "Cerrado": {"Reclasificado"},
    "Reclasificado": set(),
}

# Rangos fisiológicos (HU-E2-04): {campo: (min, max, unidad, prioritaria)}
RANGOS_SIGNOS: dict[str, tuple[float, float, str, bool]] = {
    "temperatura": (34.0, 43.0, "°C", True),
    "frecuencia_cardiaca": (20, 300, "lpm", False),
    "frecuencia_respiratoria": (4, 60, "rpm", True),
    "saturacion_o2": (50, 100, "%", True),
    "presion_sistolica": (40, 300, "mmHg", True),
    "presion_diastolica": (20, 200, "mmHg", False),
    "peso": (1.0, 400.0, "kg", False),
    "talla": (0.3, 2.5, "m", False),
}
