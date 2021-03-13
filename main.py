# Team Elote:
# Abraham Hernández Muñoz 2731337
# Oswaldo René Osuna Rangel 2794336
# Oscar Alejandro López Ramos 2842500
# Jorge Eduardo Merlo Santos 2737333
# Germán Marcelo Celestino Chávez 2866129
# Saúl Antonio Rivera Luna 2729947

# Actividad 3. Extraer palabras de archivos HTML

import time
import os
import re

# main se utiliza para arrancar el script y realiza todas las especificaciones según los requerimientos
# params: 
# tmpexe = Inicio de cronometro para medir el tiempo de ejecución total del script
# tmpexe2 = Fin del cronometro para medir el tiempo de ejecución total del script
# files = Se utiliza esta variable para obtener la localización de los archivos con los que trabajara este script
# fileholder = Sirve para guardar el nombre del archivo que se abrió, el tiempo en que tardo en abrirse, el tiempo
# para crear el nuevo archivo así como el tiempo total de ejecución y el total en crear el nuevo archivo
# totaltempfiles = Guarda el tiempo total que tardo el script para quitar todas las tags de los archivos
# tmpopen = Inicio de cronometro para medir cuanto tarda el archivo en abrirse y crear el nuevo archivo
# tmpclose = Fin del cronometro para medir cuanto tarda el archivo en abrirse y crear el nuevo archivo 
# filetime = variable que guarda el tiempo para abrir el archivo y crear el nuevo archivo del archivo 
# actual en la iteración
# txt = Se utiliza para interactuar con el archivo de texto en donde se guardarán los resultados del script

def main():
    global content
    content = []
  # tmpexe utiliza la librería de time para crear la instancia de un cronometro
    tmpexe = time.time()
  # files utiliza la librería de os para localizar los archivos con los que se trabajara
    files = os.listdir("notags")
    fileholder = ""
    totaltempfiles = 0 
  # por cada archivo en files se va a iniciar un cronometro para medir cuanto tarda en abrirse el archivo que está actualmente
  # en la iteración además de medir cuanto tiempo tarda en crear un nuevo archivo con las palabras separadas y en orden. Una vez que el 
  # cronometro se detenga se va a guardar el nombre del archivo que se abrió y el tiempo que se tardó  crear el nuevo archivo. En una 
  # variable separada se van a sumar todos los tiempos calculados(cuanto tardo en crear todos los archivos) para obtener el 
  # tiempo total para crear todos los archivos.
    for filex in files:
        create_wordlist_file(filex)
        
    
    tmpopen = time.time()
    finish()
    tmpclose = time.time()
    filetime = round(tmpclose - tmpopen,4)
    totaltempfiles += filetime

  # tmpexe2 detiene el cronometro que mide el tiempo de ejecución total
    tmpexe2 = time.time()
  # se obtiene el tiempo total para crear el nuevo archivo
    fileholder += "Tiempo total en crear el nuevo archivo consolidado: " + str(round(totaltempfiles,4)) + "\n"
  # se obtiene el tiempo de ejecución total
    fileholder += "Tiempo de ejecucion total: " + str(round(tmpexe2 - tmpexe,4))
  # se abre el archivo de texto en modo Append
    txt = open("team-elote.txt", "a")
    txt.truncate(0)
  # se escriben los datos obtenidos en este script en el archivo de texto
    txt.write(fileholder)
    txt.close()

# la función create_wordlist_file sirve para abrir los archivos y ordenar las palabras en estos
# después se guardan en una carpeta llamada wordlists
# params: 
# openedFile = Abre el archivo openedFile (el archivo actual en la iteración)
# arrayOfWords = Separa las palabras en una lista
# mylist = Guarda las palabras y las ordena
# content = Ayuda a formatear la lista
# wordlist = abre el archivo en la carpeta wordlists

# remove_html_tags(String)
def create_wordlist_file(filename):
  # abre y lee el archivo  (el archivo actual en la iteración)
    openedFile = open('notags/'+filename, 'r').read()
  # separa las palabras y simbolos del archivo en una lista
    arrayOfWords = re.split('\s+', openedFile)
    mylist = list(dict.fromkeys(arrayOfWords))
  # se ordena la lista
    mylist = sorted(mylist, key=str.lower)

  # se formatea cada palabra de la lista para que quede por renglon
    global content

    try: 
        for word in mylist:
            if word:
              content.append(word)
    except Exception as e:
        print(e)

def finish():
    global content
    sortedlist = sorted(content)
    text = ""

    try:
        for word in sortedlist:
                text += word.lower() + "\n"
        wordlist = open("wordlists/wordlist_","w")
        wordlist.truncate(0)
        wordlist.write(text)
        wordlist.close()
        print("done")
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main() 

