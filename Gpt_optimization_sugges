import cv2
import face_recognition
import os
from concurrent.futures import ThreadPoolExecutor

# Rutas y variables
ruta_directorio_archivo = os.path.dirname(os.path.abspath(__file__))
Fmodel = "cnn"  # Cambiar a 'hog' si prefieres más rapidez
Face_A_Codes = []
detected_faces_folder = "detected_faces"
folder_a = os.path.join(ruta_directorio_archivo, "A")
folder_b = os.path.join(ruta_directorio_archivo, "B")

# Crear carpeta de rostros detectados si no existe
if not os.path.exists(detected_faces_folder):
    os.makedirs(detected_faces_folder)

# Procesar las imágenes de la carpeta A
filenamea = []
for filename in os.listdir(folder_a):
    image = cv2.imread(os.path.join(folder_a, filename))
    face_locations_a = face_recognition.face_locations(image, model=Fmodel)
    
    if face_locations_a:
        face_encoding_a = face_recognition.face_encodings(image, known_face_locations=face_locations_a, model="large")[0]
        Face_A_Codes.append(face_encoding_a)
        filenamea.append(filename)

        # Guardar la imagen en la carpeta de rostros detectados
        face_folder = os.path.join(detected_faces_folder, filename)
        if not os.path.exists(face_folder):
            os.makedirs(face_folder)
        cv2.imwrite(os.path.join(face_folder, filename), image)

# Procesar imágenes de la carpeta B
def process_image_b(filename):
    image_b = cv2.imread(os.path.join(folder_b, filename))
    face_locations_b = face_recognition.face_locations(image_b, model=Fmodel)

    if face_locations_b:
        for face_location_b in face_locations_b:
            face_encoding_b = face_recognition.face_encodings(image_b, known_face_locations=[face_location_b], model="large")[0]

            # Comparar con cada rostro de la carpeta A
            results = face_recognition.compare_faces(Face_A_Codes, face_encoding_b, 0.5)

            match_found = False
            for i, match in enumerate(results):
                if match:
                    match_found = True
                    print(f"Match encontrado para {filename} con {filenamea[i]}")
                    face_folder = os.path.join(detected_faces_folder, filenamea[i])
                    cv2.imwrite(os.path.join(face_folder, filename), image_b)

            # Si no se encontró coincidencia para este rostro específico
            if not match_found:
                nf_folder = os.path.join(detected_faces_folder, "NOT_FOUND")
                if not os.path.exists(nf_folder):
                    os.makedirs(nf_folder)
                cv2.imwrite(os.path.join(nf_folder, filename), image_b)

    else:
        # Si no se encontraron rostros en la imagen
        nff_folder = os.path.join(detected_faces_folder, "NOT_FACES_FOUND")
        if not os.path.exists(nff_folder):
            os.makedirs(nff_folder)
        cv2.imwrite(os.path.join(nff_folder, filename), image_b)

# Procesar imágenes en paralelo
with ThreadPoolExecutor() as executor:
    executor.map(process_image_b, os.listdir(folder_b))

# Mostrar un mensaje de éxito al final
print("El proceso ha terminado exitosamente.")
