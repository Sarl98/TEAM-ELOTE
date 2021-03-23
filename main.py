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
import nltk
from nltk import word_tokenize

# main se utiliza para arrancar el script y realiza todas las especificaciones según los requerimientos
# params: 
# tmpexe = Inicio de cronometro para medir el tiempo de ejecución total del script
# tmpexe2 = Fin del cronometro para medir el tiempo de ejecución total del script
# files = Se utiliza esta variable para obtener la localización de los archivos con los que trabajara este script
# totaltempfiles = Guarda el tiempo total que tardo el script para quitar todas las tags de los archivos
# tmpopen = Inicio de cronometro para medir cuanto tarda el archivo en abrirse y crear el nuevo archivo
# tmpclose = Fin del cronometro para medir cuanto tarda el archivo en abrirse y crear el nuevo archivo 
# filetime = variable que guarda el tiempo para abrir el archivo y crear el nuevo archivo del archivo 
# actual en la iteración
# txt = Se utiliza para interactuar con el archivo de texto en donde se guardarán los resultados del script

def main():
  # files utiliza la librería de os para localizar los archivos con los que se trabajara
    files = os.listdir("notags")
    totaltempfiles = 0
    tokenizedFiles = ["notags_simple.html","notags_medium.html","notags_hard.html","notags_049.html"]
    allTokenizedWords =[]
    allTokenizedWordsCount = {}
  # por cada archivo en files se va a iniciar un cronometro para medir cuanto tarda en abrirse el archivo que está actualmente
  # en la iteración además de medir cuanto tiempo tarda en crear un nuevo archivo con las palabras separadas y en orden. Una vez que el 
  # cronometro se detenga se va a guardar el nombre del archivo que se abrió y el tiempo que se tardó  crear el nuevo archivo. En una 
  # variable separada se van a sumar todos los tiempos calculados(cuanto tardo en crear todos los archivos) para obtener el 
  # tiempo total para crear todos los archivos.
    tmpopen = time.time()
    for filex in files:
      if filex in tokenizedFiles:
        create_wordlist_file(filex, allTokenizedWords)

    for word in allTokenizedWords:
      if word in allTokenizedWordsCount:
        allTokenizedWordsCount[word] +=1
      else:
        allTokenizedWordsCount[word] = 1
    for word in files:
      if word in allTokenizedWordsCount:
        allTokenizedWordsCount[word] +=1
      else:
        allTokenizedWordsCount[word] = 1
    wordHold = ""
  # se escriben los datos obtenidos en este script en el archivo de texto
    for word in allTokenizedWordsCount:
      wordHold += word + " | " + str(allTokenizedWordsCount[word])
      wordHold += "\n"

    tmpclose = time.time()
    filetime = round(tmpclose - tmpopen,4)
    totaltempfiles += filetime
    wordHold += "\n" + "\n" + "Tiempo total de ejecucion: " + str(totaltempfiles)
    txt = open("team-elote.txt", "a")
    txt.truncate(0)
    txt.write(wordHold)
    txt.close()
  # se escriben los datos obtenidos en este script en el archivo de texto

# la función create_wordlist_file sirve para abrir los archivos y ordenar las palabras en estos
# después se guardan en una carpeta llamada wordlists
# params: 
# openedFile = Abre el archivo openedFile (el archivo actual en la iteración)
# arrayOfWords = Separa las palabras en una lista
# mylist = Guarda las palabras y las ordena
# content = Ayuda a formatear la lista
# wordlist = abre el archivo en la carpeta wordlists

# remove_html_tags(String)
def create_wordlist_file(filename, allTokenizedWords):
  # abre y lee el archivo  (el archivo actual en la iteración)
    openedFile = open('notags/'+filename, 'r').read()
  # separa las palabras y simbolos del archivo en una lista
    arrayOfWords = re.split('\s+', openedFile)
    mylist = list(dict.fromkeys(arrayOfWords))
  # se ordena la lista
    mylist = sorted(mylist, key=str.lower)
    mylistTokenized = []

  # se formatea cada palabra de la lista para que quede por renglon
    try: 
        for word in mylist:
            if word:
              mylistTokenized.extend(word_tokenize(word.lower()))
        finish(mylistTokenized, filename)
        allTokenizedWords.extend(mylistTokenized)
    except Exception as e:
        print(e)
      
def finish(mylistTokenized, filename):
    sortedlist = sorted(mylistTokenized)
    text = ""
    try:
        for word in sortedlist:
                text += word + "\n"
        wordlist = open("wordlists/"+ filename, "w")
        wordlist.truncate(0)
        wordlist.write(text)
        wordlist.close()
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main() 

