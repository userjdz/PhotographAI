import cv2
import face_recognition
import os
from concurrent.futures import ThreadPoolExecutor

# Rutas y variables
ruta_directorio_archivo = os.path.dirname(os.path.abspath(__file__))
Fmodel = "cnn"  # Cambiar a 'hog' si prefieres más rapidez
detected_faces_folder = "classified_faces"
folder_c = os.path.join(ruta_directorio_archivo, "C")
face_encodings_dict = {}

# Crear carpeta de clasificación si no existe
if not os.path.exists(detected_faces_folder):
    os.makedirs(detected_faces_folder)

# Procesar imágenes de la carpeta C
def process_image_c(filename):
    image_c = cv2.imread(os.path.join(folder_c, filename))
    face_locations_c = face_recognition.face_locations(image_c, model=Fmodel)

    if face_locations_c:
        for face_location_c in face_locations_c:
            face_encoding_c = face_recognition.face_encodings(image_c, known_face_locations=[face_location_c], model="large")[0]

            match_found = False
            # Buscar si el rostro ya existe en los registros
            for label, known_encoding in face_encodings_dict.items():
                if face_recognition.compare_faces([known_encoding], face_encoding_c, 0.5)[0]:
                    match_found = True
                    face_folder = os.path.join(detected_faces_folder, label)
                    if not os.path.exists(face_folder):
                        os.makedirs(face_folder)
                    cv2.imwrite(os.path.join(face_folder, filename), image_c)
                    break

            # Si no se encontró coincidencia, crear una nueva carpeta
            if not match_found:
                new_label = f"Face_{len(face_encodings_dict) + 1}"
                face_encodings_dict[new_label] = face_encoding_c
                new_face_folder = os.path.join(detected_faces_folder, new_label)
                os.makedirs(new_face_folder)
                cv2.imwrite(os.path.join(new_face_folder, filename), image_c)

    else:
        # Si no se encontraron rostros
        nff_folder = os.path.join(detected_faces_folder, "NOT_FACES_FOUND")
        if not os.path.exists(nff_folder):
            os.makedirs(nff_folder)
        cv2.imwrite(os.path.join(nff_folder, filename), image_c)

# Procesar imágenes en paralelo
with ThreadPoolExecutor() as executor:
    executor.map(process_image_c, os.listdir(folder_c))

# Mostrar un mensaje de éxito al final
print("El proceso ha terminado exitosamente.")