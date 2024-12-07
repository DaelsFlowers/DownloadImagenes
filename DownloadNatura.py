import csv
import os
import requests
from tkinter import Tk
from tkinter.filedialog import askdirectory

def descargar_imagenes(csv_path):
    Tk().withdraw()
    carpeta_destino = askdirectory(title="Selecciona una carpeta para guardar las imágenes")
    if not carpeta_destino:
        print("No se seleccionó ninguna carpeta. Salida del programa.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            id_imagen = fila['id']
            url_imagen = fila['image_url']
            nombre_archivo = f"Especie_{id_imagen}.jpg"
            ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

            try:
                respuesta = requests.get(url_imagen, stream=True)
                respuesta.raise_for_status()
                with open(ruta_archivo, 'wb') as archivo:
                    for chunk in respuesta.iter_content(1024):
                        archivo.write(chunk)
                print(f"Imagen {nombre_archivo} descargada con éxito.")
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar {url_imagen}: {e}")

if __name__ == "__main__":
    csv_path = input("Introduce la ruta del archivo CSV: ").strip()
    if os.path.exists(csv_path) and csv_path.endswith('.csv'):
        descargar_imagenes(csv_path)
    else:
        print("Archivo CSV no encontrado o no válido.")