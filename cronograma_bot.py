import tkinter as tk
import pandas as pd
from bs4 import BeautifulSoup

# Función para leer el archivo HTML y extraer los datos
def leer_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        tabla = soup.find('table')
        filas = tabla.tbody.find_all('tr')
        datos = []
        for fila in filas:
            celdas = fila.find_all('td')
            datos.append([celda.text.strip() for celda in celdas])
        return pd.DataFrame(datos, columns=['Tema de la etapa', 'Duración de la etapa', 'Objetivo de la etapa', 'Paso a paso de la etapa'])

# Función para mostrar la ventana de alerta
def mostrar_alerta(etapa):
    ventana = tk.Toplevel()
    ventana.title('Alerta')
    mensaje = tk.Label(ventana, text=f'¡Atención! Es hora de la etapa "{etapa}"')
    mensaje.pack()
    boton_ok = tk.Button(ventana, text='OK', command=ventana.destroy)
    boton_ok.pack()

# Función principal para procesar los datos y mostrar las alertas
def procesar_cronograma(file_path):
    # Leer el archivo HTML y extraer los datos
    df = leer_html(file_path)

    # Crear la ventana principal
    root = tk.Tk()
    root.title('Cronograma de la Clase')

    # Crear el widget de tabla con los datos
    tabla = tk.Label(root, text=df.to_string(index=False), justify='left')
    tabla.pack()

    # Configurar las alertas para cada etapa
    for i, fila in df.iterrows():
        duracion = int(fila['Duración de la etapa'].split()[0])
        etapa = fila['Tema de la etapa']
        root.after(duracion*1000*60, mostrar_alerta, etapa)

    # Mostrar la ventana principal
    root.mainloop()

# Ejemplo de uso
procesar_cronograma('./Roblox_M1L2_tabla.html')
