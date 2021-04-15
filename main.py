# Team Elote:
# Abraham Hernández Muñoz 2731337
# Oswaldo René Osuna Rangel 2794336
# Oscar Alejandro López Ramos 2842500
# Jorge Eduardo Merlo Santos 2737333
# Germán Marcelo Celestino Chávez 2866129
# Saúl Antonio Rivera Luna 2729947

# Actividad 9

import time
import sys
import os
import re
from typing import Dict
import nltk
from nltk import word_tokenize

# Empieza y ejecuta el programa.
#
# Variables locales: 
# - files = abre los archivos que se utilizarán.
# - allTokenizedWordsCountPerFile = Diccionario que contendrá las palabras, incluyendo la cantidad
# 	de archivos en las que esta palabra aparece. También contendrá cuáles son los archivos en los 
# 	que aparece y la frecuencia en las que aparece en ese archivo.
# - tmpOpen = Inicia el timer.
# - tmpClose = Cierra el timer.
# - totalTimeCount = Mensaje del tiempo total del contador.
#
# main()
def main():
	# Abre la carpeta "notags" y devuelve nombre de todos los archivos que contiene.
	files = os.listdir("notags")
	allTokenizedWordsCountPerFile = {}
	tmpOpen = time.time()

	# Si no existen los archivos de palabras tokenizadas en la carpeta "wordlists" los crea.
	createFileIfDontExist(files)
	# Genera el diccionario de las palabras tokenizadas.
	getTokenizedLists(allTokenizedWordsCountPerFile)
	# Crea el documento de posting.txt.
	createPostingFile(allTokenizedWordsCountPerFile)
	# Crea el documento de diccionario.txt.
	createDictionaryFile(allTokenizedWordsCountPerFile)

	tmpClose = time.time()
	totalTimeCount = "\n\n Tiempo total de ejecucion del programa: " + str(round(tmpClose - tmpOpen, 4))

	# Agrega el tiempo total de ejecución al archivo a10_matricula.txt.
	createFile("a10_matricula.txt", totalTimeCount, False)

# createFileIfDontExist sirve para validar si el archivo existe en la carpeta "wordlists" 
# y crear los archivos necesarios si estos no existen. Toma el tiempo de creación de
# cada archivo.
#
# Parámetros:
# - files = Lista de los archivos de "notags".
#
# Variables locales:
# - fileTimeOpen = Inicio del contador.
# - fileTimeClose = Fin del contador.
# - timeCountString = String que contiene el tiempo de ejecución de todos los archivos que se crearon.
#
# createFileIfDontExist(list[string])
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

	# Creamos el archivo de texto diccionario.txt.
	createFile("tiempos-de-creacion-wordlists.txt", timeCountString, True)

# getTokenizedLists se encarga de leer los archivos de la carpeta "wordlists"
# y crea un diccionario con las palabras y el número de archivos en las que 
# aparecen. También obtiene cuáles son los archivos en los que aparece la palabra
# y la frecuencia en la que esta aparece en ese archivo.
#
# Params:
# - allTokenizedWordsCountPerFile = Diccionario donde se guardan las palabras
#   y la cantidad de archivos en las que aparecen.
#
# Variables locales:
# - sortedFiles = Lista de todos los archivos en la carpeta "wordlists".
# - openedFile = Abre y lee el archivo actual.
# - listOfWords = Lista que contiene las palabras tokenizadas del archivo.
# - repeatedWords = Lista de las palabras que ya aparecieron en el archivo actual.
# - timeLogContent = String que contiene los logs de tiempo de cada archivo.
# - tmpOpen = Inicia el timer.
# - tmpClose = Cierra el timer.
# - timeLogContent = Mensaje del tiempo total del contador.
# - stopList = Lista de palabras que no pueden incluirse.
#
# getTokenizedLists(dict[string: int])
def getTokenizedLists(allTokenizedWordsCountPerFile):
	sortedFiles = os.listdir("wordlists")
	timeLogContent = ""
	#Conseguimos lista de palabras del Stop List
	stopList = getListOfWords("stop_list.html")
	# Por cada archivo...
	for file in sortedFiles:
		# Abrimos el contador de tiempo.
		tmpOpen = time.time()
		listOfWords = getListOfWords("wordlists/"+file)
		repeatedWords = []

		# Por cada palabra en la lista myList...
		for word in listOfWords:
			#Si la palabra no se encuentra en la lista y la palabra es de mas de un caracter...
			if(word not in stopList) and (len(word) > 1):
				# Si la palabra no está en la lista de palabras repetidas Y
				# no está en el diccionario de allTokenizedWordsCountPerFile...
				if (word not in repeatedWords) and (word not in allTokenizedWordsCountPerFile):
					allTokenizedWordsCountPerFile[word] = {}
					# Se añade la palabra al diccionario con un valor inicial de 1.
					allTokenizedWordsCountPerFile[word]["count"] = 1
					# Inicializamos el diccionario de files.
					allTokenizedWordsCountPerFile[word]["files"] = {}
					# Inicializamos el contador de la palabra en el archivo con un
					# valor inicial de 1.
					allTokenizedWordsCountPerFile[word]["files"][file] = 1

					# Se añade la palabra a la lista de palabras repetidas.
					repeatedWords.append(word)
				# Si la palabra no está en la lista de palabras repetidas Y
				# si está en el diccionario de allTokenizedWordsCountPerFile...
				elif (word not in repeatedWords) and (word in allTokenizedWordsCountPerFile):
					# Se le suma 1 a la cuenta.
					allTokenizedWordsCountPerFile[word]["count"] += 1
					# Se añade la palabra a la lista de palabras repetidas.
					repeatedWords.append(word)
				# Si la palabra se repite...
				elif (word in repeatedWords):
					# Si el archivo no está inicializado en el diccionario...
					if file not in allTokenizedWordsCountPerFile[word]["files"]:
						# Se inicializa con un valor inicial de 1.
						allTokenizedWordsCountPerFile[word]["files"][file] = 1
					# Si el archivo sí está inicializado en el diccionario...
					else:
						# Le sumamos uno a su contador de frecuencia.
						allTokenizedWordsCountPerFile[word]["files"][file] += 1
		# Cerramos el contador de tiempo.
		tmpClose = time.time()
		# Concatenamos el mensaje de tiempo del archivo.
		timeLogContent += file + "   " + str(round(tmpClose - tmpOpen, 4)) + "\n"
	# Se crea un archivo con las palabras tokenizadas (Facilita el uso de los comandos en commands.py)
	createFile("tokenizedWords.txt", str(allTokenizedWordsCountPerFile), True)	
	# Creamos el archivo que registra el tiempo.
	createFile("a10_matricula.txt", timeLogContent, True)
			
# createPostingFile se encarga de crear el archivo posting.
#
# Parámetros:
# - allTokenizedWordsCountPerFile: Diccionario de palabras con su cantidad de
#   archivos en los que aparece y el diccionario de archivos en los que esa
#	palabra aparece y la cantidad de veces que aparece ahí.
#
# Variables locales:
# - postingFileContent = String que forma el contenido del archivo posting.
# - wordsToRemove = Palabras que se borraran del diccionario por no cumplir con ciertos parametros...
# - wordWeight = guarda el peso total de la palabra en el archivo actual
# createPostingFile(list[dict[])
def createPostingFile (allTokenizedWordsCountPerFile):
	postingFileContent = ""
	wordsToRemove = []
	# Por cada palabra dentro del diccionario allTokenizedWordsCountPerFile...
	for word in allTokenizedWordsCountPerFile:
		#Si la frecuencia de palabras es mayor a 2...
		if(allTokenizedWordsCountPerFile[word]["count"] > 2):
			# Por cada fileName dentro de el diccionario de archivos de esa palabra...
			for fileName in allTokenizedWordsCountPerFile[word]["files"]:
				wordWeight = 0
				wordWeight = weight(allTokenizedWordsCountPerFile, word, fileName)
				# Formamos el string y se lo concatenamos a postingFileContent...
				postingFileContent += fileName + " | " + str(wordWeight) + "\n"
		#Si la frecuencia de palabras es menor a 2...
		else:
			#Agrega la palabra al listado de palabras que se eliminaran 
			wordsToRemove.append(word)
	#Por cada palabra dentro de wordsToRemove
	for word in wordsToRemove:
		#Saca la palabra del diccionario
		allTokenizedWordsCountPerFile.pop(word)		

	# Creamos el archivo de texto posting.txt.
	createFile("posting.txt", postingFileContent, True)
	
# createDictionaryFile se encarga de crear el archivo diccionario.
#
# Parámetros:
# - allTokenizedWordsCountPerFile = Diccionario de palabras con su cantidad de
#   archivos en los que aparece y el diccionario de archivos en los que esa
#	palabra aparece y la cantidad de veces que aparece ahí.
#
# Variables locales:
# - dictionaryFileContent = String que forma el contenido del archivo diccionario.
# - postingIndex = Contador del índice relativo a posting.
# - hashtable = Diccionario(Estructura Python) que almacena los datos de cada palabra
#   en una estructura similar al HashTable.
#
# createDictionaryFile(list[dict[])
def createDictionaryFile (allTokenizedWordsCountPerFile):
	dictionaryFileContent = ""
	postingIndex = 0
	hashtable = {}
	# Por cada palabra en el diccionario de allTokenizedWordsCountPerFile...
	for word in allTokenizedWordsCountPerFile:

		# Verificamos si la palabra puede ser codificada en codigo ascii para añadirla a
		# la hashtable, si no lo es agregamos un 0 y -1.
		if is_ascii(word):
			# Concatenamos a dictionaryFileContent la cantidad de archivos en las
			# que aparece y el índice relativo a posting.
			dictionaryFileContent += "'" + word + "' | " + str(allTokenizedWordsCountPerFile[word]["count"]) + " | " + str(postingIndex) + "\n"
			# Agregamos cada iteracion a la hashtable, la key sera la palabra y el count e indice posting
			# seran el valor.
			hashtable[word] = [allTokenizedWordsCountPerFile[word]["count"],postingIndex]
		else:
			dictionaryFileContent += "    " + "|    0|    -1"+ "\n"
		# Guardamos los datos en una estructura HashTable para acceder a ellos mediante una key.
		# Sumamos al contador de postingIndex la cantidad de archivos en las que
		# aparece.
		postingIndex += len(allTokenizedWordsCountPerFile[word]["files"])

	# Hacemos un encode ascii a nuestro diccionario.

	# Creamos el archivo de texto diccionario.txt.
	createFile("diccionario.txt", dictionaryFileContent, True)

# is_ascii sirve para corrobarar si una cadena o caracter puede ser encoded en ascii.
#
# Parámetros:
# - text = Cadena de texto a revisar.
def is_ascii(text):
	# Primero descomponemos la cadena de texto mediante un for.
	# Despues usamos la funcion ord que regresa un integer representando el caracter Unicode para
	# verificar si es ascii.
    return all(ord(c) < 128 for c in text)

# createTokenizedList abre el archivo actual de la carpeta "notags" y crea una lista de
# las palabras del archivo y las tokeniza.
#
# Parámetros:
# - filename = Nombre del archivo actual.
#
# Variables locales:
# - myListTokenized = Lista de las palabras tokenizadas de este archivo.
# - openedFile = Abre y lee el archivo actual.
# - listOfWords = Lista que contiene las palabras tokenizadas del archivo.
# - myList = Lista que remueve los tokens repetidos.
#
# createTokenizedList(string)
def createTokenizedList(filename):
	myListTokenized = []
	
	# Abre el archivo.
	openedFile = open('notags/'+filename, 'r').read()
	# Separa las palabras en el archivo.
	listOfWords = re.split('\s+', openedFile)
	# Se crea una lista con las palabras separadas.
	myList = list(dict.fromkeys(listOfWords))

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
# y crea un nuevo archivo en la carpeta "wordlists" con estas token.
# 
# Parámetros:
# - mylistTokenized = Lista con todas las palabras tokenizadas del archivo actual.
# - filename = El nombre del archivo.
#
# Variables locales:
# - fullFileContentString = String con todas las palabras del archivo actual.
#
# createWordlistFile(list[string], string)
def createWordlistFile(mylistTokenized, filename):
	fullFileContentString = ""
	
	# Ordena alfabéticamente la lista.
	mylistTokenized.sort()

	try:
		# Por cada palabra en la lista mylistTokenized...
		for word in mylistTokenized:
			# Le concatena la palabra a fullFileContentString y da un enter.
			fullFileContentString += word + "\n"

		# Creamos el archivo de texto diccionario.txt.
		createFile("wordlists/"+ filename, fullFileContentString, True)

	except Exception as e:
		print(e)

# createFile crea el archivo y lo guarda con el nombre y contenido dado.
#
# Parámetros:
# - fileName = Nombre del archivo.
# - fileContent = Contenido del archivo.
# - willTruncate = Determina si se borrará el contenido del archivo antes
#   de escribir sobre él.
#
# Variables locales:
# - txt = Abre el archivo y lo guarda.
#
# createFile(string, string, bool)
def createFile(fileName, fileContent, willTruncate):
	# Abre el archivo.
	txt = open(fileName, "a")

	if willTruncate:
		# Vacía el archivo.
		txt.truncate(0)
		
	# Añade el string postingFileContent al archivo.
	txt.write(fileContent)
	# Lo cierra y guarda.
	txt.close()


# getListOfWords es una funcion que regresa una lista de palabras de un archivo ordenado
# Parámetros:
# -file = Archivo ordenado
# Variables locales:
# - openedFile = Variable que almacena al archivo como string
#   getListOfWords(String)
def getListOfWords(file):
	openedFile = open(file, 'r', encoding='windows-1252').read()
	return re.split('\s+', openedFile)

# weight devuelve el peso final de la palabra tomando en cuenta la cantidad de tokens que hay en el documento actual y las
# veces que se repite en este
#
# params:
# - allTokenizedWordsCountPerFile = diccionario  de palabras
# - word = palabra actual de la cual se va a devolver el peso
# - filename = archivo actual
# 
# variables locales:
# - weight = peso final de la palabra en el documento
# - listOfWords = lista de todas las palabras en el documento
# - filteredTokenlist = lista de todas las palabras en el documento quitando las palabras repetidas
# - listLen = longitud de la lista "filteredTokenlist"
# 
# returns:
# - weight = peso final de la palabra en el documento
#
# weight(list[dict[], String, String)
def weight(allTokenizedWordsCountPerFile, word, filename):
  weight = 0
  listOfWords = getListOfWords("wordlists/" + filename)
  filteredTokenlist = list(dict.fromkeys(listOfWords))
  listLen = len(filteredTokenlist)
  weight = round(allTokenizedWordsCountPerFile[word]['files'][filename] * 100 / listLen, 4)

  return weight
if __name__ == "__main__":
	main() 