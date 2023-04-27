import cv2
import face_recognition
import os
ruta_directorio_archivo = os.path.dirname(os.path.abspath(__file__))
Fmodel="cnn"
Face_A_Codes=[]
Face_A_Code_index=0
face_loc =[]
image=[]
filenamea=[]
face_locations=[]
 # Carpeta donde se guardarán las detecciones de los rostros
detected_faces_folder = "detected_faces"
if not os.path.exists(detected_faces_folder):
    os.makedirs(detected_faces_folder)
# Ruta de la carpeta "a"
folder_a = os.path.join(ruta_directorio_archivo,"A")
for filename in os.listdir(folder_a):

    # Cargar la imagen
    filenamea.append(filename)
    #print(filename)
    image = (cv2.imread(os.path.join(folder_a, filename)))
    #print("imagen leida")
    face_loc= (face_recognition.face_locations(image)[0])
    #print("rostro detectado")
    Face_A_Codes.append(face_recognition.face_encodings(image, known_face_locations=[face_loc], model="large")[0])
    #print("rostro codificado")
    face_folder = os.path.join(detected_faces_folder, f"{filename}")
    if not os.path.exists(face_folder):
        os.makedirs(face_folder)
    cv2.imwrite(os.path.join(face_folder, filename), image)
    

folder_b = os.path.join(ruta_directorio_archivo,"B")
for filename in os.listdir(folder_b):
    # Cargar la imagen
    found=False
    imageC = cv2.imread(os.path.join(folder_b, filename))
    print("imagen: ", filename,"  leida")
    face_locations = face_recognition.face_locations(imageC)
    print("posiciones de rostros: ",face_locations)
    if face_locations == []:
        nff_folder =os.path.join(os.path.join(ruta_directorio_archivo,"detected_faces"),"NOT_FACES_FOUND")
        if not os.path.exists(nff_folder):
            os.makedirs(nff_folder)
        cv2.imwrite(os.path.join(nff_folder, filename), imageC)
    if face_locations != []:
          for face_location in face_locations:
               Face_B_Code = face_recognition.face_encodings(imageC, known_face_locations=[face_location], model= "large")[0]
               Face_A_Code_index=0
               for Face_A_Code in Face_A_Codes:
                    result = face_recognition.compare_faces([Face_A_Code], Face_B_Code,0.5)
                    if result[0] == True:
                        found=True
                        print("--------------------MATCH-----------------------------")
                        face_folder= os.path.join(os.path.join(ruta_directorio_archivo,"detected_faces"),filenamea[Face_A_Code_index])
                        print(face_folder)
                        print(Face_A_Code_index)
                        print(filename)
                        #reponer el face folder en la siguiente linea
                        cv2.imwrite(os.path.join(face_folder, filename), imageC)
                    Face_A_Code_index +=1
        
    #En caso de no encontrar la persona en la imagen, va a NOT_FOUND
    if not found:
        nf_folder =os.path.join(os.path.join(ruta_directorio_archivo,"detected_faces"),"NOT_FOUND")
        if not os.path.exists(nf_folder):
            os.makedirs(nf_folder)
        cv2.imwrite(os.path.join(nf_folder, filename), imageC)
        

                
# Mostrar un mensaje de éxito al final
print("El proceso ha terminado exitosamente.")            
