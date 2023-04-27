import cv2
import os

# Ruta de la carpeta "a"
folder_a = "C:/Users/julia/OneDrive/Escritorio/IA/PhotografAI/A"

# Carpeta donde se guardarán las detecciones de los rostros
detected_faces_folder = "detected_faces"

# Cargar el detector de rostros (Haar Cascade)
face_cascade = cv2.CascadeClassifier("C:\\users\\julia\\appdata\\local\\programs\\python\\python310\\lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")

# Recorrer las imágenes en la carpeta "a"
for filename in os.listdir(folder_a):
    # Cargar la imagen
    image = cv2.imread(os.path.join(folder_a, filename))
    
    # Convertir a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros en la imagen
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Recorrer los rostros detectados
    for (x, y, w, h) in faces:
        # Recortar la región del rostro
        face = image[y:y + h, x:x + w]
        
        # Guardar la detección en una carpeta específica
        face_folder = os.path.join(detected_faces_folder, f"face_{x}_{y}_{w}_{h}")
        if not os.path.exists(face_folder):
            os.makedirs(face_folder)
        cv2.imwrite(os.path.join(face_folder, filename), face)

# Ruta de la carpeta "b"
folder_b = "C:/Users/julia/OneDrive/Escritorio/IA/PhotografAI/B"

# Recorrer las imágenes en la carpeta "b"
for filename in os.listdir(folder_b):
    # Cargar la imagen
    image = cv2.imread(os.path.join(folder_b, filename))
    
    # Convertir a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros en la imagen
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Recorrer los rostros detectados
    for (x, y, w, h) in faces:
        # Recortar la región del rostro
        face = image[y:y + h, x:x + w]
        
       # Buscar la carpeta correspondiente
        found = False
        for face_folder in os.listdir(detected_faces_folder):
            # Calcular la similitud entre la cara detectada y la cara guardada en la carpeta
            saved_face_path = os.path.join(detected_faces_folder, face_folder, filename)
            if os.path.exists(saved_face_path):
                # Cargar la imagen guardada
                saved_face = cv2.imread(saved_face_path)

                #reescala las dimenciones y canales para calcular la diferencia 
                rows, cols, channels = saved_face.shape
                face = cv2.resize(face, (cols, rows))
                
                # Calcular la diferencia entre la cara detectada y la cara guardada
                difference = cv2.absdiff(face, saved_face)
                difference = cv2.sumElems(difference)
                
                # Verificar si la diferencia es menor a un umbral
                if difference[0] + difference[1] + difference[2] < 5000:
                    # Guardar la imagen en la carpeta correspondiente
                    cv2.imwrite(os.path.join(face_folder, filename), face)
                    found = True
                    break

        # Si no se encontró una cara correspondiente, guardar en una carpeta "no_match"
        if not found:
            no_match_folder = os.path.join(detected_faces_folder, "no_match")
            if not os.path.exists(no_match_folder):
                os.makedirs(no_match_folder)
            cv2.imwrite(os.path.join(no_match_folder, filename), face)
        # Cerrar la imagen
        cv2.destroyAllWindows()


        
# Mostrar un mensaje de éxito al final
print("El proceso ha terminado exitosamente.")
