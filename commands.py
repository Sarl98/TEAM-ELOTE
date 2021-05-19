import argparse
import nltk
import ast
import os
from flask import Flask, render_template
from flask import request
from main import *
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/', methods=['POST'])
def my_link():
  projectpath = request.form['projectFilepath']
  hl = main(projectpath)
  '<a href = "'

  myString = "Resultados de la busqueda de " + projectpath + ":" +"<br/>"

  for el in hl:
    dictionaryFile = open("wordlists/" + str(el), "r")
    myUrl = '"' + os.path.realpath(dictionaryFile.name) + '"' 

    myString += "<a href = "+ myUrl + ">" + el + "</a>" + " " + str(hl[el]) +"<br/>"

  return myString

def main(projectpath):
    
    userSearch = []
    search = projectpath
    
    # Separa las palabras en el archivo.
    listOfWords = re.split('\s+', search)
	# Se crea una lista con las palabras separadas.
    userSearch = list(dict.fromkeys(listOfWords))
    print(search)

    if(userSearch):
        fileTimeOpen = time.time()
        foundOne = False
        limit = 10
        n = 0

        # Forma el string del log.
        logText = "\n# Resultados para " + str(userSearch) + "\n"
        print(logText)
        mainfolderLocation = Path(__file__).absolute().parent
        evidenciaFileLocation = str(mainfolderLocation) + '/evidencia.txt'
        evidenciaFile = open(evidenciaFileLocation, "r").read()
         # Separa las palabras en el archivo.
        listOfTokenizedSplits = re.split(' ---', evidenciaFile)
        # Se crea una lista con las palabras separadas.
        listOfTokenizedWordsWithWeights = list(dict.fromkeys(listOfTokenizedSplits))

        holderList = {}

        for word in userSearch:
            for evidenciaRow in listOfTokenizedWordsWithWeights:
                if (word in evidenciaRow):
                    index = re.findall('notags\_\d.*\.html', evidenciaRow)[0]
                    if (index in holderList):                        
                        holderList[index] += float(re.sub(r'[\s\S].* \| ', '', evidenciaRow))
                    else:
                        holderList[index] = float(re.sub(r'[\s\S].* \| ', '', evidenciaRow))
            
        # resultsList = []
        # for holderVal in holderList:
        #     resultsList.append(holderList[holderVal])

        # resultsList.sort(reverse=True)
          
        for holder in holderList:
          # dictionaryFile = open("wordlists/" + str(file), "r")
          print(holder + " " + str(holderList[holder]))
        fileTimeClose = time.time()
        timeCountString = ("Se tardo en encontrar: " + str(round(fileTimeClose - fileTimeOpen, 4)) + " segundos\n")
        print(timeCountString)  

        return holderList
        
if __name__ =="__main__":
    app.run(debug=True)