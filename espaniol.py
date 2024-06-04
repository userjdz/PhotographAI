import cv2
import face_recognition
import os

# Ruta del directorio del archivo actual
ruta_directorio_archivo = os.path.dirname(os.path.abspath(__file__))

# Modelo de detección de rostros
modelo_deteccion = "cnn"

# Listas para almacenar los códigos de reconocimiento facial y otros datos
codigos_rostros_a = []
indice_codigo_rostro_a = 0
ubicaciones_rostros = []
imagenes = []
nombres_archivos_a = []

# Carpeta donde se guardarán las detecciones de los rostros
carpeta_rostros_detectados = "detected_faces"
if not os.path.exists(carpeta_rostros_detectados):
    os.makedirs(carpeta_rostros_detectados)

# Ruta de la carpeta "A" (Fotos únicas de los graduados)
carpeta_a = os.path.join(ruta_directorio_archivo, "A")
for nombre_archivo in os.listdir(carpeta_a):
    # Cargar la imagen
    nombres_archivos_a.append(nombre_archivo)
    imagen = cv2.imread(os.path.join(carpeta_a, nombre_archivo))
    ubicacion_rostro = face_recognition.face_locations(imagen)[0]
    codigos_rostros_a.append(face_recognition.face_encodings(imagen, known_face_locations=[ubicacion_rostro], model="large")[0])
    carpeta_rostro = os.path.join(carpeta_rostros_detectados, f"{nombre_archivo}")
    if not os.path.exists(carpeta_rostro):
        os.makedirs(carpeta_rostro)
    cv2.imwrite(os.path.join(carpeta_rostro, nombre_archivo), imagen)

# Ruta de la carpeta "B" (todas las fotos a ordenar)
carpeta_b = os.path.join(ruta_directorio_archivo, "B")
for nombre_archivo in os.listdir(carpeta_b):
    # Cargar la imagen
    encontrado = False
    imagen_b = cv2.imread(os.path.join(carpeta_b, nombre_archivo))
    print("Imagen: ", nombre_archivo, " leída")
    ubicaciones_rostros_b = face_recognition.face_locations(imagen_b)
    print("Posiciones de rostros: ", ubicaciones_rostros_b)
    if not ubicaciones_rostros_b:
        carpeta_no_rostros = os.path.join(carpeta_rostros_detectados, "NOT_FACES_FOUND")
        if not os.path.exists(carpeta_no_rostros):
            os.makedirs(carpeta_no_rostros)
        cv2.imwrite(os.path.join(carpeta_no_rostros, nombre_archivo), imagen_b)
    else:
        for ubicacion_rostro_b in ubicaciones_rostros_b:
            codigo_rostro_b = face_recognition.face_encodings(imagen_b, known_face_locations=[ubicacion_rostro_b], model="large")[0]
            indice_codigo_rostro_a = 0
            for codigo_rostro_a in codigos_rostros_a:
                resultado_comparacion = face_recognition.compare_faces([codigo_rostro_a], codigo_rostro_b, 0.5)
                if resultado_comparacion[0]:
                    encontrado = True
                    print("--------------------MATCH-----------------------------")
                    carpeta_rostro = os.path.join(carpeta_rostros_detectados, nombres_archivos_a[indice_codigo_rostro_a])
                    print(carpeta_rostro)
                    print(indice_codigo_rostro_a)
                    print(nombre_archivo)
                    cv2.imwrite(os.path.join(carpeta_rostro, nombre_archivo), imagen_b)
                indice_codigo_rostro_a += 1

    # En caso de no encontrar la persona en la imagen, va a NOT_FOUND
    if not encontrado:
        carpeta_no_encontrado = os.path.join(carpeta_rostros_detectados, "NOT_FOUND")
        if not os.path.exists(carpeta_no_encontrado):
            os.makedirs(carpeta_no_encontrado)
        cv2.imwrite(os.path.join(carpeta_no_encontrado, nombre_archivo), imagen_b)

# Mostrar un mensaje de éxito al final
print("El proceso ha terminado exitosamente.")
