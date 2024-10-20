import yaml

config_route = "config.yml"
material = '\n\n**El Origen del Ser Humano**\n\n* El ser humano surge en África, hace aproximadamente 2,5 millones de años.\n* Las primeras formas humanas eran similares a los primates actuales, pero a lo largo del tiempo evolucionaron y se desarrollaron en diferentes especies.\n* La especie más primitiva es la Australopiteco, que era bípeda y se alimentaba de frutas y verduras.\n* La especie más avanzada es el Homo sapiens, que es la especie actual del ser humano.\n* El clima y el entorno geográfico jugaron un papel importante en la evolución del ser humano.\n* La competencia por los recursos y la adaptación al medio ambiente influyeron en el desarrollo de las habilidades y tecnologías humanas.\n\n'
config = yaml.safe_load(open("config.yml"))