import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
import shutil
import os
import requests
import rarfile
from pathlib import Path
import pandas as pd

def plt_table(df, file, titl,titl_fs,table_fs):
    # Convertir el DataFrame a una lista de listas
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(8.5, 11), tight_layout=True)

    # Ocultar ejes
    ax.axis('off')

    # Crear la tabla
    tabla = ax.table(cellText=data_list, bbox=[0, 0.1, 1, 0.8])

    # Ajustar el tamaño de las celdas
    tabla.auto_set_font_size(False)

        # Establecer el tamaño de la fuente para la tabla
    tabla.set_fontsize(table_fs)

    # Dar formato a las celdas
    for key, cell in tabla.get_celld().items():
        if key[0] == 0:  # Formato para la fila de encabezados
            cell.set_text_props(weight='bold', color='white', horizontalalignment='center')  # Texto en negrita, color blanco y centrado
            cell.set_facecolor('#2a3d4f')  # Color de fondo
        else:  # Formato para las celdas de datos
            cell.set_facecolor('#d9d9d9')  # Color de fondo gris claro
            cell.set_text_props(horizontalalignment='center')  # Centrar el texto en las 

    

    # Agregar título al gráfico con tamaño de letra y posición ajustados
    ax.set_title(titl, fontsize=titl_fs, fontweight='bold',y=0.91)  

    return fig

def pie_chart(df,file,titl,titl_fs,l_fs):
    # Crear una figura y un eje para el gráfico de torta
    fig, ax = plt.subplots(figsize=(8.5, 11), tight_layout=True)  # Tamaño de página carta

    # Datos para el gráfico de torta
    datos_agrupados = df.value_counts()
    # Definir el explode para separar cada porción del centro
    explode = [0.05] * len(datos_agrupados)
    # Crear el gráfico de torta con los datos agrupados
    # y especificar las etiquetas y los colores
    porciones, etiquetas, autopct = ax.pie(datos_agrupados, autopct=lambda p: f'{p:.1f}%\n({int(p * sum(datos_agrupados)/100)})', pctdistance=1.12,  
                                        textprops={'horizontalalignment': 'center', 'verticalalignment': 'center', 'fontsize': 15},
                                        startangle=0.50, radius=1,explode=explode)

    # Agregar título al gráfico con tamaño de letra y posición ajustados
    ax.set_title(titl, loc='center', fontsize=titl_fs, fontweight='bold')  

    # Agregar leyenda debajo del gráfico de torta
    ax.legend(labels=datos_agrupados.index, loc="upper right", fontsize=l_fs, framealpha=0.8)

    # Quitar los ejes
    ax.axis('off')

    return fig

def create_directory(path):
        # Crear un objeto Path
    directory = Path(path)

    # Verificar si el directory existe
    if directory.exists():
        # Eliminar el directory si ya existe
        shutil.rmtree(directory)
        print(f"directory '{path}' eliminado.")

    # Crear el directory
    directory.mkdir(parents=True)
    print(f"directory '{path}' creado con éxito.")


def download_file(path,url_file,name_file):
        # Realizar la solicitud GET para descargar el archivo
    response = requests.get(url_file, stream=True)

    # Verificar si la descarga fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Crear el archivo en la carpeta de destino
        destination_path = os.path.join(path, name_file)
        with open(destination_path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print("Descarga exitosa. El archivo se ha guardado en:", destination_path)
    else:
        print("No se pudo descargar el archivo.")

def load_first_csv(file_csv,path):
    if file_csv:
        first_csv = file_csv[0]  # Obtén el primer archivo CSV
        path_csv = os.path.join(Path(path), first_csv)  # Obtén la ruta completa del archivo
        df = pd.read_csv(path_csv,sep=";")  # Lee el archivo CSV y carga los datos en un 
        df=homologation(df)

        print("El primer archivo CSV se ha cargado en un DataFrame.")
    else:
        print("No se encontraron archivos CSV en el directory especificado.")
    return df


def unrar_file(path_file,destination_path):
    with rarfile.RarFile(path_file, 'r') as rf:
        # Extraer todos los archivos
        rf.extractall(destination_path)



def homologation(df):

    new_col_names = {'nomb_carrera': 'CARRERA', 'nomb_inst': 'INSTITUCIÓN','gen_alu': 'GÉNERO','nivel_carrera_2':'TIPO TÍTULO','region_sede':'REGIÓN'}
    # Renombrar las columnas
    df = df.rename(columns=new_col_names)

    # Define el diccionario de mapeo de valores
    carr_change = carr_names()

    # Aplica el reemplazo en la columna especificada usando el método replace()
    df['CARRERA'] = df['CARRERA'].replace(carr_change)

    # Definir el mapeo de palabras clave a abreviaturas
    replace_carr = {
        'TECNICO': 'TEC.',
        'INGENIERIA': 'ING.',
        #'ADMINISTRACION': 'ADM.',
        'EJECUCION': 'EJEC.',
        'LICENCIATURA': 'LICEN.'
    }

    # Crear una expresión regular para buscar las palabras clave
    patron = '|'.join(replace_carr.keys())

    # Realizar el reemplazo utilizando expresiones regulares
    df['CARRERA'] = df['CARRERA'].str.replace(patron, lambda x: replace_carr[x.group()], regex=True)



    # Define el diccionario de mapeo de valores
    inst_change = inst_names()

    # Aplica el reemplazo en la columna especificada usando el método replace()
    df['INSTITUCIÓN'] = df['INSTITUCIÓN'].replace(inst_change)


    # Definir el mapeo de palabras clave a abreviaturas
    replace_inst = {
        'PONTIFICIA': '',
        'UNIVERSIDAD': 'UNIV.'
    }

    # Realizar el reemplazo utilizando expresiones regulares
    df['INSTITUCIÓN'] = df['INSTITUCIÓN'].str.replace(patron, lambda x: replace_inst[x.group()], regex=True)



    # Aplica el reemplazo en la columna especificada usando el método replace()
    df['GÉNERO'] = df['GÉNERO'].replace({1:'HOMBRE',2:'MUJER'})

    return df

def inst_names():
    name_list={
        'UNIVERSIDAD TECNOLOGICA DE CHILE INACAP':'INACAP',
        'UNIVERSIDAD SANTO TOMAS':'UNIV. SANTO TOMAS',
        'UNIVERSIDAD ANDRES BELLO':'UNIV. ANDRES BELLO',
        'IP LATINOAMERICANO DE COMERCIO EXTERIOR - IPLACEX':'IP IPLACEX',
        'UNIVERSIDAD DE ANTOFAGASTA':'UNIV. ANTOFAGASTA',
        'UNIVERSIDAD DE LAS AMERICAS':'UNIV. DE LAS AMÉRICAS',
        'PONTIFICIA UNIVERSIDAD CATOLICA DE CHILE':'UNIV. CATÓLICA',
        'UNIVERSIDAD DE PLAYA ANCHA DE CIENCIAS DE LA EDUCACION':'UNIV. DE PLAYA ANCHA',
        'UNIVERSIDAD TECNOLOGICA METROPOLITANA':'UTEM',
        'UNIVERSIDAD CENTRAL DE CHILE':'UCEN',
        'UNIVERSIDAD CATOLICA DE TEMUCO':'UNIV. CATÓLICA DE TEMUCO',
        'UNIVERSIDAD DE SANTIAGO DE CHILE':'USACH',
        'IP INSTITUTO SUPERIOR DE ARTES Y CIENCIAS DE LA COMUNICACION':'IP INST. SUPERIOR DE ARTES',
        'UNIVERSIDAD AUTONOMA DE CHILE':'UNIV. AUTÓNOMA DE CHILE',
        'UNIVERSIDAD DEL DESARROLLO':'UNIV. DEL DESARROLLO',
        'UNIVERSIDAD TECNICA FEDERICO SANTA MARIA':'UNIV. FEDERÍCO SANT. MARÍA',
        'UNIVERSIDAD IBEROAMERICANA DE CIENCIAS Y TECNOLOGIA, UNICIT':'UNICIT',
        'UNIVERSIDAD CATOLICA CARDENAL RAUL SILVA HENRIQUEZ':'UNIV. CATOL. SILVA HENRIQUEZ',
        'PONTIFICIA UNIVERSIDAD CATOLICA DE VALPARAISO':'UNIV. CATÓLICA DE VALP.',
        'UNIVERSIDAD CATOLICA DE LA SANTISIMA CONCEPCION':'UNIV: CATÓLICA DE VALPAR.'}
    return name_list


def carr_names(): 
    name_list = {
        'INGENIERIA EN MAQUINARIA, VEHICULOS AUTOMOTRICES Y SISTEMAS ELECTRONICOS': 'ING. MAQ. VEHIC. AUTO',
        'INGENIERIA EN MECANICA AUTOMOTRIZ Y AUTOTRONICA': 'ING. MECANICA AUT.',
        'INGENIERIA EN ADMINISTRACION DE RECURSOS HUMANOS': 'ING. ADMIN. DE RECUR. HUMA.',
        'INGENIERIA EN ADMINISTRACION DE EMPRESAS MENCION FINANZAS': 'ING ADM. EMP.',
        'INGENIERIA EN ADMINISTRACION': 'ING. ADMINISTRACION',
        'INGENIERIA EN PREVENCION DE RIESGOS': 'ING. PREV. RIESGOS',
        'INGENIERIA DE EJECUCION EN ADMINISTRACION DE EMPRESAS MENCION FINANZAS': 'ING. DE EJEC. ADM. EMP. M. F',
        'INGENIERIA DE EJECUCION EN ADMINISTRACION DE EMPRESAS MENCION RECURSOS HUMANOS': 'ING ADM. EMP.',
        'INGENIERIA EN PREVENCION DE RIESGOS, CALIDAD Y AMBIENTE': 'ING. PREV. RIESGOS',
        'PEDAGOGIA EN EDUCACION DIFERENCIAL CON ESPECIALIDAD EN DISCAPACIDAD INTELECTUAL': 'PEDAG. EDUC. DIFERENCIAL',
        'PEDAGOGIA EN EDUCACION DIFERENCIAL': 'PEDAG. EDUC. DIFERENCIAL',
        'PROFESOR DE EDUCACION DIFERENCIAL CON MENCION EN LENGUAJE': 'PROF. EDUC. DIFERENCIAL',
        'ADMINISTRACION PUBLICA, MENCION GESTION Y DESARROLLO REGIONAL Y LOCAL': 'ADM. PUBLICA',
        'PEDAGOGIA EN EDUCACION FISICA': 'PEDG. EDUCACION FISICA',
        'INGENIERIA CIVIL CON MENCIONES / INGENIERIA CIVIL DE INDUSTRIAS CON MENCION': 'ING. CIVIL DE INDUSTRIAS',
        'PEDAGOGIA EN EDUCACION BASICA MENCION LENGUAJE O MATEMATICAS': 'PEDG. EDUCACION BASICA',
        'INGENIERIA EN MAQUINARIA Y VEHICULOS AUTOMOTRICES SIN MENCION': 'ING. MAQ. VEHIC. AUTO',
        'FORMACION DE PROFESORES DE EDUCACION GENERAL BASICA': 'PEDG. EDUCACION BASICA',
        'PEDAGOGIA EN EDUCACION BASICA': 'PEDG. EDUCACION BASICA',
        'INGENIERIA EN MAQUINARIA Y VEHICULOS AUTOMOTRICES': 'ING. MAQ. VEHIC. AUTO',
        'PEDAGOGIA EN EDUCACION GENERAL BASICA': 'PEDG. EDUCACION BASICA',
        'PROFESOR DE EDUCACION GENERAL BASICA, LICENCIADO EN EDUCACION': 'PEDG. EDUCACION BASICA',
        'INGENIERIA EJECUCION EN ADMINISTRACION DE EMPRESAS': 'ING. EJEC. ADM. EMP.',
        'LICENCIATURA EN CIENCIAS CRIMINALISTICAS': 'LIC. CIENCIAS CRIMINALISTICA',
        'INGENIERIA DE EJECUCION EN ADMINISTRACION DE EMPRESAS': 'ING. EJEC. ADM. EMP.',
        'INGENIERIA EN CONSTRUCCION': 'ING. CONSTRUCCION',
        'INGENIERIA MECANICA EN MANTENIMIENTO INDUSTRIAL': 'ING. MECANICA EN MANTENIMIENTO',
        'INGENIERIA CIVIL INDUSTRIAL': 'ING. CIVIL INDUSTRIAL',
        'INGENIERIA EN INFORMATICA': 'ING. EN INFORMATICA',
        'TECNICO DE NIVEL SUPERIOR EN EDUCACION PARVULARIA': 'TEC. EN EDUCACION PARVULARIA',
        'TECNICO EN ADMINISTRACION DE EMPRESAS MENCION RECURSOS HUMANOS':'TEC. EN ADM. EMPRESAS',
        'MECANICA AUTOMOTRIZ EN SISTEMAS ELECTRONICOS':'MECANICA AUTOM. EN SIST. ELECTR',
        'TECNICO EN ENFERMERIA MENCION EN URGENCIA':'TEC. EN ENFERMERIA',
        'TECNICO EN ENFERMERIA MEDICA':'TEC. EN ENFERMERIA',
        'TECNICO DE NIVEL SUPERIOR EN ENFERMERIA':'TEC. EN ENFERMERIA'
    }
    return name_list

