from preprocess import preprocessMidi
from models import getModel
from sklearn.model_selection import train_test_split
import numpy as np
import sys,getopt

batch_size = 20
defaultSaveName = "unnamed.h5"
dataDirName = "MIDI/test"

def importDataSet(dirName):
	print(":: IMPORTING DATA SET")
	X,y = preprocessMidi(dirName,verbose=1,removeExceptions=True,max_sample_len=batch_size,allowMultipleNotesOnTempo=False,allowNoteOnSeveralTempos=False)
	if len(X) == 0:
		raise Exception("The sample is empty.")
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20)
	print("Data set splitted into train and test data")
	return X_train,X_test,y_train,y_test

def compileModel(model):
	print(":: COMPILING MODEL")
	model.compile(loss='mse',optimizer='rmsprop')

def fitModel(model,X,y):
	print(":: FITTING MODEL")
	model.fit(X,y,nb_epoch=5)

def evalModel(model,X,y):
	print(":: EVALUATING MODEL ON TEST DATA")
	loss = model.evaluate(X,y)
	print("Loss : "+str(loss))

def useModel(model,modelSaveName,dataDir):
	X_train,X_test,y_train,y_test = importDataSet(dataDir)
	compileModel(model)
	fitModel(model,X_train,y_train)
	evalModel(model,X_test,y_test)
	model.save(modelSaveName)

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'test.py -i <dataDirName> -o <modelSaveName>'
		sys.exit(2)
	saveName = defaultSaveName
	for opt, arg in opts:
		if opt == '-i':
			dataDirName = arg
		elif opt == '-o':
			saveName = arg
	model = getModel(batch_size)
	useModel(model,saveName,dataDirName)
	if saveName == defaultSaveName:
		print("Please be carefull, your saved model has a default name!")


if __name__ == "__main__":
	main(sys.argv[1:])
