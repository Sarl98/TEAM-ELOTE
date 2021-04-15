import argparse
import nltk
import ast
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