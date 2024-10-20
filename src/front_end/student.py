LECCIONES = [
    {
        "pregunta": """### La Era de la Prehistoria
            * La prehistoria es el período de tiempo que comprende desde la aparición del primer ser humano hasta la invención de la escritura.
            * Durante la prehistoria, los seres humanos se desarrollaron y se extendieron por todo el mundo, lo que se conoce como el poblamiento de los continentes.
            * La prehistoria se divide en tres grandes períodos: Paleolítico (hace 2,5 millones de años hasta hace 10.000 años), Mesolítico (hace 10.000 años hasta hace 5.000 años) y Neolítico (hace 5.000 años hasta hace 2.000 años).
            * Durante la prehistoria, los seres humanos se dedicaron a la caza y la recolección de alimentos, hasta que se desarrolló la agricultura y la ganadería.
            * La domesticación de plantas y animales permitió a los seres humanos establecerse en un lugar y formar comunidades más grandes.
            * La prehistoria nos deja un legado en forma de herramientas de piedra, pinturas rupestres y otros objetos que nos ayudan a entender cómo vivían nuestros antepasados.
            """,
        "respuesta": ""
    },
    {
        "pregunta": """### El Origen del Ser Humano
            * El ser humano surge en África, hace aproximadamente 2,5 millones de años.
            * Las primeras formas humanas eran similares a los primates actuales, pero a lo largo del tiempo evolucionaron y se desarrollaron en diferentes especies.
            * La especie más primitiva es la Australopiteco, que era bípeda y se alimentaba de frutas y verduras.
            * La especie más avanzada es el Homo sapiens, que es la especie actual del ser humano.
            * El clima y el entorno geográfico jugaron un papel importante en la evolución del ser humano.
            * La competencia por los recursos y la adaptación al medio ambiente influyeron en el desarrollo de las habilidades y tecnologías humanas.
            """,
         "respuesta": "" 
    },
    {
        "pregunta": """### La Sedentarización y el Origen de las Ciudades
            * La sedentarización se refiere al proceso de establecerse en un lugar permanentemente y abandonar la vida nómada.
            * La domesticación de plantas y animales permitió a los seres humanos producir alimentos de manera más eficiente y establecerse en un lugar.
            * Las primeras ciudades surgieron en el Neolítico, hace aproximadamente 5.000 años.
            * Las ciudades se convirtieron en centros de comercio, cultura y gobierno.
            * La invención de la escritura permitió a los seres humanos registrar eventos, leyes y tradiciones, lo que facilitó la organización social y política.
            * Las primeras ciudades se caracterizaron por la concentración de población, la especialización laboral y la formación de clases sociales.
            """,
         "respuesta": ""
    }
            
]

PREGUNTAS = [
     {
        "pregunta": "## ¿Cuál es el período de tiempo que comprende la prehistoria?",
        "respuesta": "La prehistoria es el período de tiempo que comprende desde la aparición del primer ser humano hasta la invención de la escritura."
    },
    {
        "pregunta": "## ¿Cómo se llaman los tres grandes períodos en que se divide la prehistoria?",
        "respuesta": "La prehistoria se divide en Paleolítico, Mesolítico y Neolítico."
    },
    {
        "pregunta": "## ¿Por qué la domesticación de plantas y animales permitió a los seres humanos establecerse en un lugar y formar comunidades más grandes?",
        "respuesta": "La domesticación de plantas y animales permitió a los seres humanos producir alimentos de manera más eficiente y establecerse en un lugar de manera permanente."
    }
]

EXAMEN = [
     {
        "pregunta": "# ¿Dónde surge el ser humano según lo dicho en clase?",
        "respuesta": "El ser humano surge en África."
     },
     {
        "pregunta": "# ¿Cuáles son las tres grandes divisiones de la prehistoria?",
        "respuesta": "La prehistoria se divide en Paleolítico, Mesolítico y Neolítico."
     },
     {
        "pregunta": "# ¿Qué facilitó a los seres humanos producir alimentos de manera más eficiente y establecerse en un lugar?",
        "respuesta": "La domesticación de plantas y animales."
     },
     {
        "pregunta": "# ¿Qué período de tiempo comprende la prehistoria?",
        "respuesta": "Desde la aparición del primer ser humano hasta la invención de la escritura."
     },
     {
          "pregunta": "# ¿Por qué la sedentarización se refiere a establecerse en un lugar permanentemente?",
          "respuesta": "La sedentarización se refiere a establecerse en un lugar permanentemente y abandonar la vida nómada."
     }
]

class Student:
    def __init__(self):
        self.id = 1
        self.actual = 0
        self.interaccion = False
        self.conversation = []
        self.actual_material = "lecciones"
        self.lecciones = LECCIONES
        self.preguntas = PREGUNTAS
        self.examen = EXAMEN
        self.content = self.lecciones
        self.header = f"## Clase {self.actual + 1}"
      