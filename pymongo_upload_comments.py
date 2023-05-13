from pymongo_get_database import get_database


encuentro1 = {
    "nombre" : "Paseo exploratorio 1",
    "url" : "https://www.decidim.barcelona/processes/avingudamadrid/f/4880/meetings/5208",
    "comentarios" : ["Me gustaría participar. De verdad que no hay plazas? Al menos me gustaría tener un email a quién comentar mis reflexiones. Soy vecino de la calle Berlín y desde luego que hay muchas cosas que mejorar.",
    "Yo estoy apuntada para el lunes 14 pero no podré ir, te cedo mi plaza"
    ]
}
encuentro2 = {
    "nombre" : "Paseo exploratorio 2",
    "url" : "https://www.decidim.barcelona/processes/avingudamadrid/f/4880/meetings/5211",
    "comentarios" : ["Gràcies per la 'Passejada exploratòria 2' que avui he fet amb vosaltres."]
}
encuentro3 = {
    "nombre" : "Sessión de constitución de la Comissión de Seguimiento",
    "url" : "https://www.decidim.barcelona/processes/avingudamadrid/f/4880/meetings/4958",
    "comentarios" : ["Me gustaria participar en lacomisión a título individual (como vecina). ¿Es posible?.",
    "Hola Gema, en primer lugar, perdona por el retraso. A priori en la Comisión de Seguimiento se proponen entidades como asociaciones de vecinos, comerciales, sociales y culturales del entorno para ofrecer una visión amplia del territorio. En todo caso, vamos a contactarte por e-mail para informarte de todos los espacios y acciones participativas que prevemos desarrollar durante este proceso para ver si alguna se ajusta a tus intereses y valorar también la posibilidad de incorporarte en la Comisión de Seguimiento.",
    "Gracias, ya recibí vuestro email!",
    "Molt bé !!!! Endavant amb aquesta iniciativa de re-urbanització de l'avinguda de Madrid. Ja feia anys que tocava. Es una avinguda (tram Brasil-Pl.Centre) que esta igual que la va deixar l'Alcalde franquista Porcioles. 'Desarrollisme' en estat pur - urbanisme al servei exclussiu del cotxe-. Endavant amb mes espai pels vianants i amb carril bici. Tot el suport !!!",
    "Hola! Podríem integrar-nos dues veïnes (per molt que no tinguem una entitat constituïda) a la comissió de seguiment?",
    "D'igual manera que a l'avinguda Madrid, els veïns i les veïnes del carrer Berlín, patim els efectes més nocius de la contaminació en totes les seves dimensions: pol·lució, brutícia, soroll acústic i un espai abandonat per a la ciutadania on només predominen els vehicles. S'haurien d'ampliar les voreres, reduir com a mínim a 3 carrils de circulació, crear 2 carrils bici, habilitar una vèrtebra veritablement verda per a la ciutat i l'apropament dels barris de Sants i Les Corts. Si hem de projectar la ciutat del futur i més concretament aquest espai que ocupem, hem d'atendre aquests criteris. Imaginar la ciutat verda destinada als vianants i a la ciutadania, pensada per els i les qui la vivim. Reduir a 4 carrils de circulació és una fugida endavant que ens pot costar molt cara. Ha d'haver-hi un màxim de 3, amb grans arbredes i espais per al nostre gaudir.",
    ]
}
Reurbanizacion_Avenida_Madrid = {
  "_id" : "avingudamadrid",
  "encuentros" : [encuentro1, encuentro2, encuentro3]
  }




encuentro4 = {
    "nombre" : "Sesión abierta de debate de diagnosis y propuesta",
    "url" : "https://www.decidim.barcelona/processes/interiorsdillaGuineueta/f/5568/meetings/6345",
    "comentarios" : ["Si pueden poner la opción de castellano",
    "Tiene la opción de cambiar la lengua al castellano en la parte superior de la pantalla"
    ]
}
Reurbanizacion_Guineueta = {
  "_id" : "interiorsdillaGuineueta",
  "encuentros" : [encuentro4]
  }




  
encuentro5 = {
    "nombre" : "Paseo exploratorio",
    "url" : "https://www.decidim.barcelona/processes/parcoreneta/f/5419/meetings/6130",
    "comentarios" : ["Por favor, avisar de cambios en la visita por email. Hasta entonces. Muchas gracias por el interés en el parque."]
}
encuentro6 = {
    "nombre" : "Sesión inicial de debate del proceso Participativo del Plan Director del Parc del Castell de l'Oreneta",
    "url" : "https://www.decidim.barcelona/processes/parcoreneta/f/5419/meetings/6061",
    "comentarios" : ["Tot el conflicte respecte a l'oposició a la urbanització (drenatges urbans, pavimentació, deteriorament de la vegetació, els béns patrimonials) i la pavimentació del Parc Forestal del Castell de l'Oreneta tenen la seva base en les irregularitats detectades per part de la taula de contractació de BIMSA, incompliment normatiu i el contingut del Projecte Executiu dirigit per un enginyer de camins, canals i ports i no per un equip d'arquitectes biòlegs i paisatgistes. Altrament, la pèrdua de la qualificació urbanística 27 (Parc forestal) per 6 (Zona verda) ha permès el deteriorament del parc. La proposta és senzilla: no es pot redactar un Pla Director amb cara i ulls si no es canvia la qualificació urbanística i el retorn al Parc Natural de la Serra de Collserola del que mai hauria d'haver estat segregat. Sense aquest canvi, tot és paper mullat. Aquesta proposta té el suport de la Plataforma Cívica per a la Defensa de Collserola (PCDC) i les entitats que en formen part.",
    "La contractació s'ha dut a terme seguint el Marc normatiu de contractació pública vigent. Podeu consultar l'expedient a la Plataforma electrònica de contractació Pública de la Generalitat de Catalunya: https://contractaciopublica.gencat.cat/ecofin_pscp/AppJava/ca_ES/awardnotice.pscp?idDoc=85227108&reqCode=viewDcan (Link externo). El Consorci de Collserola va fer un informe en relació amb el Parc, on es feien alguns comentaris que es van recollir en el disseny del projecte. Quant a la qualificació urbanística, aquesta data del 1978 i aquesta qualificació no té res a veure amb la seva degradació. No és preceptiu canviar la qualificació per poder redactar un Pla Director.",
    "Quan era petita, anar al Parc de l’Oreneta era una aventura; era anar a una muntanya plena de vida. A mida que em vaig fer gran, la muntanya s’anava pelant i es deterioraven totes les restes patrimonials del Parc. Hi va haver un bar, una zona de ponis i un jardí amb escultures precioses d’Hongria, que també van desaparèixer. Va aparèixer una pedrera i noves zones de parc infantil. Els veïns mai hem sabut el criteri aplicat per fer aparèixer/desaparèixer tots aquests espais que han existit al parc. El que sí sabem és que pavimentar-lo ha estat un despropòsit, i més de la forma com s’ha fet (sense informació pública, sense aplicar criteris de respecte mediambiental, ni ecològics, ni patrimonials, per citar només alguns). Cal que això no torni a passar mai més. Consensuem usos i criteris per a que tots entenguem el perquè de les actuacions que es facin. Fem que el Parc torni a ser una muntanya, la nostra muntanya -ara ferida- del Collserola",
    "El Parc s'ha anat degradant, per una manca d'inversió en anys, en un espai utilitzat com a parc urbà; tant la xarxa de drenatge, com els sistemes de contenció de terres o sistemes de reg per assentar les plantacions han quedat obsolets. Les finques originals del Parc eren terrenys agrícoles, no forestals. Aquest fet va motivar la necessitat de fer una actuació per frenar l'erosió i millorar-ne l'estat general (objecte del projecte). Les concessions de bar que hi ha hagut en el passat van tancar per decisió pròpia. El servei de ponis es va tancar perquè no complia la normativa de benestar animal. Quant al jardí amb escultures hongareses, no era un jardí sinó una àrea de jocs que, a mesura que aquests elements de joc s'han anat degradant per les inclemècies del temps, s'han anat eliminant per motius de seguretat. Quant al consens d'usos i criteris, hem previst una sèrie d'accions participatives a partir del mes de gener que ens permetran debatre aquests criteris i usos del Parc.",
    "El passat 23 de nov. vaig assistir a la sessió de constitució de la Comissió de Seguiment del procés participatiu del Pla Director al Centre i Teatre de Sarrià. Com sempre te per costum el Districte, no hem rebut cap acta. Durant la sessió es varen demanar una sèrie d'aclariments amb motiu de diferents preocupacions que es van exposar. Per la meva vaig demanar la participació amb l'equip redactor del pla per poder aportar tot el coneixement i experiència professional en temes urbanístics, constructius i històrics atès que tinc molta documentació i dades històriques de la finca del castell per ser besnet dels antics propietaris. També vaig expressar la meva preocupació amb les diferents qualificacions urbanístiques que actualment apareixen en el àmbit del pla i que prèviament es tindrien que revisar per evitar possibles actuacions viaries i de planejament que podrien desvirtuar la condició de Parc Forestal. En aquest sentit amb ratifico en el que ha exposat el company Jordi Bigues",
    "L'acta de la Sessió de constitució de la Comissió de Seguiment del passat 23 de novembre la podeu trobar penjada al Decidim a la mateixa trobada (Constitución de la Comisión de Seguimiento). També s'ha enviat un correu indicant aquest enllaç. Pel que fa a l'aportació de coneixement i experiència, hem previst una sèrie d'entrevistes al mes de gener amb aquelles entitats i persones que disposin de documentació escrita o d'informació oral i ens la vulguin fer arribar.",
    "Aprofito aquesta finestra per recordar a la Gerència del Districte que en la última reunió d'obra de finals de Juliol en la que vaig ser l'únic assistent fora dels representants del Districte, Bimsa, Parcs i Jardins, la Direcció de l'Obra i el Constructor Faus, aquesta Gerència es va comprometre a enviar-me l'acta de la reunió i els documents del tancament pressupostàri de l'obra, partida per partida, per així poder fer la recepció formal de l'obra i la seva finalització. He demanat també aquesta documentació a la responsable de comunicació del Districte, obtenint per resposta que ho comunicaria a la Gerència. Podrem algun dia revisar les partides reals i modificades in situ de tots els bunyols que s'han fet a les obres de Millora del Parc de l'Oreneta LOT 2 ??",
    "La reunió a la qual feu referència va ser una visita d'obra en què es van prendre algunes notes però no hi s'ha aixecat cap acta. Pel que fa a les partides que comenteu, un cop l'obra s'hagi tancat podreu consultar l'expedient al portal de Transparència de l'Ajuntament de Barcelona."
    ]
}
PlanDirector_CastellOroneta = {
  "_id" : "parcoreneta",
  "encuentros" : [encuentro5,encuentro6]
  }


  
dbname = get_database()
collection_name = dbname["ProcesosParticipativos"]
collection_name.insert_many([Reurbanizacion_Avenida_Madrid, Reurbanizacion_Guineueta, PlanDirector_CastellOroneta])