# PhotographAI
Herramienta para la identificación de rostros  

Esta herramienta está destinada a la clasificación de imagenes por medio de reconocimiento facial.

Para instalar la herramienta y usarla, asegurate de tener instalato Python en tu equipo, puedes descarlo de https://www.python.org/downloads/
Posteriormente, para windows ejecuta el archivo  "Instalacion.bat".
Si eres usuario de MAC, ejecuta los siguientes comandos en la terminal: 

python3 -m ensurepip

pip install opencv-python

pip install opencv-contrib-python

pip install imutils

pip install CMake

pip install face-recognition


# Comó usar el programa
Una vez instalado, cree una carpeta llamada "A" junto a el archivo PhotographAI.py y ponga dentro de esta las fotos de los rostros a buscar (idealmente debe estar el rostro descubierto y DEBE aparecer solo UNA persona en cada imagen. Se recomienda usar imagenes con buena resolucion). Tenga en cuenta que el nombre que tenga cada imagen será el nombre que tendrá cada carpeta en la que se almacenen los resultados posteriormente (si su imagen de llama "IMG_001.JPG", la carpeta en la cual se almacenará los rostros que coincidan con dicha imagen, se llamará "IMG_001.JPG").

Posteriormente, de la misma manera cree una catpeta llamada "B" y almacene allí las imagenes a organizar.

Ahora es momento de ejecutar el archivo "PhotographAI.py" y esperar a que finalice, momento en el cual imprimirá "El proceso ha terminado exitosamente.", los resultados los encontraremos en la carpeta que se ha creado, llamada "detected_faces", en donde se encontrarán separadas por carpetas cada coincidencia encontrada, tambien encontrará allí la carpeta "NOT_FOUND", en la cual se encontrarán los rostros que el programa no pudo reconocer...

ADVERTENCIA: Hasta el momento la deteccion de rostros no es perfecta, se recomienda una revision humana a cada una de las carpetas de los resultados con el fin de depurar dichos resultados. 

Nota: Esta es hasta el momento la primera y más primitiva version funcional de este proyecto, cualquier clase de recomendacion para mejorar será gratamente aceptada.
