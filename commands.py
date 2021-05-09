import argparse
import nltk
import ast
import os
from main import *

# commands genera los comandos y lee los argumentos
#
# Variables locales:
# - parser = Funcion de argparser para generar comandos
# - args = Argumentos que pueden ser leidos en la linea de comandos.
#
# commands()
def commands():
    parser=argparse.ArgumentParser(description="Tokenizar o indexar")
    parser.add_argument("-tok",help="tokenizar",dest="tok",action='store_false',required=False)
    parser.add_argument("-ind",help="indexar",dest="ind",action='store_false',required=False)
    parser.add_argument('-search',action="extend", metavar='name', type=str, nargs='+',
                    help='busca archivos con esta palabra',required=False)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

# run manda a llamar funciones de main.py dependiendo del argumento que pongas
# En caso de no conocer los comandos usa -h
#
# Variables locales:
# - allTokenizedWordsCountPerFile = Palabras tokenizadas (Las consigue de main.py)
# - args = Argumentos que pueden ser leidos en la linea de comandos.
#
# run(argumentos)

def run(args):
    
    if(args.search):
        fileTimeOpen = time.time()
        foundOne = False
        limit = 10
        n = 0

        # Forma el string del log.
        logText = "\n# Resultados para " + str(args.search) + "\n"
        print(logText)

        # Por cada archivo en el directorio wordlists.
        for file in os.listdir("wordlists"):
            # Si supera el limit...
            if (n > limit):
                # Sale del bucle.
                break;

            # Abre el archivo del wordlists actual.
            dictionaryFile = open("wordlists/" + str(file), "r")
            # Extrae la lista de palabras del archivo.
            dictonary = dictionaryFile.read()

            # Si todas las palabras de la búsqueda están dentro del archivo
            # devuelve verdadero, sino falso.
            allIn = all(arg in dictonary for arg in args.search)

            # Si sí las contiene todas...
            if (allIn):
                # Marca que sí encontró una coincidencia.
                foundOne = True

                # Concatena el mensaje del texto al log.
                coincidenceLogText = "Coincidencias encontradas en el archivo: ['" + file + "']\n"
                logText += coincidenceLogText

                # Imprime el mensaje.
                print(coincidenceLogText)
                # Aumenta el contador de palabras
                n += 1            

            # Se limpia el buffer en memoria del archivo actual.
            dictionaryFile.flush()
            # Se cierra el archivo.
            dictionaryFile.close()

        fileTimeClose = time.time()
        timeCountString = ("Se tardo en encontrar: " + str(round(fileTimeClose - fileTimeOpen, 4)) + " segundos\n")
        print(timeCountString)  
        if(not foundOne):
            # Concatena el mensaje del texto al log.
            coincidenceLogText = "No se encontro en ningun archivo"
            logText += coincidenceLogText

            print(coincidenceLogText)
            timeCountString = timeCountString + "no se encontro ningun archivo con el token brindado"
          
        # Crea los archivos de logs.
        createFile("tiempos-de-busqueda-wordlists.txt", timeCountString, True)
        createFile("a13_elotes.txt", logText, False)

    if(args.tok == False):
        print("Creando Tokens")
        allTokenizedWordsCountPerFile = {}
        getTokenizedLists(allTokenizedWordsCountPerFile)
        print("Archivo tokenizado creado con exito!")
        
    if(args.ind == False):    
        try:
            print("Creando Indice (El proceso toma un tiempo)")
            allTokenizedWordsCountPerFile = open("tokenizedWords.txt", "r").read()
            allTokenizedWordsCountPerFile = ast.literal_eval(allTokenizedWordsCountPerFile)
            createPostingFile(allTokenizedWordsCountPerFile)
            print("Se indexo con exito!")
        except IOError:
            print("No hay palabras tokenizadas, prueba correr el comando -tok")
        
if __name__ =="__main__":
    commands()    