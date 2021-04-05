# Team Elote:
# Abraham Hernández Muñoz 2731337
# Oswaldo René Osuna Rangel 2794336
# Oscar Alejandro López Ramos 2842500
# Jorge Eduardo Merlo Santos 2737333
# Germán Marcelo Celestino Chávez 2866129
# Saúl Antonio Rivera Luna 2729947

# Actividad 7

import time
import os
import re
from typing import Dict
import nltk
from nltk import word_tokenize

# Empieza y ejecuta el programa.
# Params: 
# files = abre los archivos que se utilizarán.
#
def main():
	# Abre la carpeta "notags" y devuelve nombre de todos los archivos que contiene.
	files = os.listdir("notags")
	allTokenizedWords = []
	allTokenizedWordsCount = {}
	allTokenizedWordsPerFile = []
	allTokenizedWordsCountPerFile = {}
	tmpopen = time.time()

	# Si no existen los archivos de palabras tokenizadas en la carpeta "wordlists" los crea.
	createFileIfDontExist(files)
	getTokenizedLists(allTokenizedWords, allTokenizedWordsPerFile)
	
	for word in allTokenizedWords:
		if word in allTokenizedWordsCount:
			allTokenizedWordsCount[word] +=1
		else:
			allTokenizedWordsCount[word] = 1

	for tokenizedWord in allTokenizedWordsPerFile:
		word = tokenizedWord.split(".-.")
		word = word[0]

		if word in allTokenizedWordsCountPerFile:
			allTokenizedWordsCountPerFile[word] += 1
		else:
			allTokenizedWordsCountPerFile[word] = 1

	fullWordList = {}

	dictIdent = 0
	dictKeys = ["word", "countGeneral", "countPerFile"]

	for tokenizedWord in allTokenizedWordsPerFile:
		word = tokenizedWord.split(".-.")
		word = word[0]
		
		fullWordList[dictIdent] = {}

		fullWordList[dictIdent][dictKeys[0]] = word
		fullWordList[dictIdent][dictKeys[1]] = str(allTokenizedWordsCount[word])
		fullWordList[dictIdent][dictKeys[2]] = allTokenizedWordsCountPerFile[word]

		dictIdent += 1

	wordHold = ""

	for i in fullWordList:
		wordHold += fullWordList[i][dictKeys[0]] + " | " + str(fullWordList[i][dictKeys[1]]) + " | " + str(fullWordList[i][dictKeys[2]])
		wordHold += "\n"

	tmpclose = time.time()
	filetime = round(tmpclose - tmpopen,4)
	totaltempfiles = 0
	totaltempfiles += filetime
	wordHold += "\n" + "\n" + "Tiempo total de ejecucion: " + str(totaltempfiles)
	txt = open("team-elote.txt", "a")
	txt.truncate(0)
	txt.write(wordHold)
	txt.close()

# createFileIfDontExist sirve para validar si el archivo existe en la carpeta "wordlists" y crear
# los archivos necesarios si estos no existen. Toma el tiempo de creación de cada archivo.
#
# Parámetros:
# - files = Lista de los archivos de "notags".
# Variables locales:
# - fileTimeOpen = Inicio del contador.
# - fileTimeClose = Fin del contador.
# - timeCountString = String que contiene el tiempo de ejecución de todos los archivos que se crearon.
#
# createFileIfDontExist(list[string], list[string], list[string], string)
def createFileIfDontExist(files):
	timeCountString = ""
	
	# Por cada archivo en la carpeta de notags...
	for filex in files:
		# Si el archivo no ha sido creado anteriormente...
		if not os.path.isfile("wordlists/" + filex):
			# Inicia un timer.
			fileTimeOpen = time.time()
			# Crea una lista de tokens para el archivo actual, ordenado alfabéticamente 
			# y crea un nuevo archivo en la carpeta de "wordlists".
			createTokenizedList(filex)
			# Cierra el timer.
			fileTimeClose = time.time()

			# Agrega ese tiempo al archivo de tiempos.
			timeCountString += (filex + " se tardo en generar: " + str(round(fileTimeClose - fileTimeOpen, 4)) + " segundos\n")
		# Si el archivo ha sido creado anteriormente...
		else:
			# Le asigna un tiempo de 0 segundos.
			timeCountString += filex + " se tardo en generar: 0 segundos\n"

	# Abre el archivo.
	txt = open("a6_matricula.txt", "a")
	# Vacía el archivo.
	txt.truncate(0)
	# Añade el string timeCountString al archivo.
	txt.write(timeCountString)
	# Lo cierra y guarda.
	txt.close()


def getTokenizedLists(allTokenizedWords, allTokenizedWordsPerFile):
	# Lista de todos los archivos en la carpeta "wordlists".
	sortedFiles = os.listdir("wordlists")

	# Por cada archivo...
	for file in sortedFiles:
		# Abre el archivo.
		openedFile = open('wordlists/'+file, 'r').read()
		# Separa las palabras en el archivo.
		arrayOfWords = re.split('\s+', openedFile)
		# Se crea una lista con las palabras separadas.
		myList = list(dict.fromkeys(arrayOfWords))
		# Agrega la lista de palabras tokenizadas del archivo actual a la lista de
		# todas las palabras tokenizadas de todos los archivos.
		allTokenizedWords.extend(myList)

		# Por cada palabra en la lista myList...
		for word in myList:
			# Le concatena a la palabra el nombre del archivo en el que se encuentra.
			concatenatedWord = word + ".-." + file

			# Si concatenedWord no está en la lista allTokenizedWordsPerFile...
			if concatenatedWord not in allTokenizedWordsPerFile:
				# Se añade a la lista.
				allTokenizedWordsPerFile.append(concatenatedWord)
			

# createTokenizedList abre el archivo actual de la carpeta "notags" y crea una lista de
# las palabras del archivo y las tokeniza.
#
# Parámetros:
# - filename = Nombre del archivo actual.
# - allTokenizedWords = Lista con todas las palabras tokenizadas de todos los archivos.
#
# createTokenizedList(string, list[string], list[string])
def createTokenizedList(filename):
	myListTokenized = []
	
	# Abre el archivo.
	openedFile = open('notags/'+filename, 'r').read()
	# Separa las palabras en el archivo.
	arrayOfWords = re.split('\s+', openedFile)
	# Se crea una lista con las palabras separadas.
	myList = list(dict.fromkeys(arrayOfWords))

	try:
		# Por cada palabra en la lista myList...
		for word in myList:
			# Si la palabra no está vacía...
			if word:
				# Se añade a la lista myListTokenized y la convierte a minúscula.
				myListTokenized.extend(word_tokenize(word.lower()))

		# Envía la lista myListTokenized a la función createWordlistFile para crear
		# el documento en la carpeta "wordlists" del archivo actual que contiene la
		# lista ordenada de los tokens.
		createWordlistFile(myListTokenized, filename)

	except Exception as e:
		print(e)
		

# createWordlistFile crea una lista de todas las tokens del archivo actual
# y crea un nuevo archivo en la carpeta "wordlists" con estas token
# 
# Parámetros:
# - mylistTokenized = Lista con todas las palabras tokenizadas del archivo actual.
# - filename = El nombre del archivo.
# - allTokenizedWordsPerFile = Lista con las palabras tokenizadas concatenadas con
#   el nombre del archivo actual.
#
# Variables locales:
# - fullFileContentString = String con todas las palabras del archivo actual.
# - concatenatedWord = String con el nombre de la palabra unido al nombre del archivo.
# - wordlist = Archivo actual en la carpeta "wordlists".
#
# createWordlistFile(list[string], string, list[string])
def createWordlistFile(mylistTokenized, filename):
	fullFileContentString = ""
	
	# Ordena alfabéticamente la lista.
	mylistTokenized.sort()

	try:
		# Por cada palabra en la lista mylistTokenized...
		for word in mylistTokenized:
			# Le concatena la palabra a fullFileContentString y da un enter.
			fullFileContentString += word + "\n"

		# Abre el archivo en la carpeta de wordlists. Si este no existe, lo crea.
		wordlist = open("wordlists/"+ filename, "w")
		# Vacía el contenido del archivo.
		wordlist.truncate(0)
		# Añade el string fullFileContentString en el archivo.
		wordlist.write(fullFileContentString)
		# Lo cierra y lo guarda.
		wordlist.close()

	except Exception as e:
		print(e)

if __name__ == "__main__":
  main() 