from preprocess import preprocessMidi
from models import getModel
from sklearn.model_selection import train_test_split
from keras.models import load_model
import numpy as np
import sys,getopt
import datetime as dt

batch_size = 20
dataDirName = "MIDI/test"

def importDataSet(dirName):
	print(":: IMPORTING DATA SET")
	X,y = preprocessMidi(dirName,verbose=0,removeExceptions=True,
							max_sample_len=batch_size,
							allowMultipleNotesOnTempo=False,
							allowNoteOnSeveralTempos=False)
	if len(X) == 0:
		raise Exception("The sample is empty.")
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20)
	print("Data set splitted into train and test data")
	return X_train,X_test,y_train,y_test

def compileModel(model):
	print(":: COMPILING MODEL")
	model.compile(loss='mse',optimizer='rmsprop',metrics=['accuracy'])

def fitModel(model,X,y):
	print(":: FITTING MODEL")
	model.fit(X,y,nb_epoch=20)

def evalModel(model,X,y):
	print(":: EVALUATING MODEL ON TEST DATA")
	metrics = model.evaluate(X,y)
	for i in range(len(metrics)):
		print(model.metrics_names[i]+" : "+str(metrics[i]))

def useModel(model,modelSaveName,dataDir):
	X_train,X_test,y_train,y_test = importDataSet(dataDir)
	compileModel(model)
	fitModel(model,X_train,y_train)
	evalModel(model,X_test,y_test)
	#model.save(modelSaveName)
	model.save_weights(modelSaveName)

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"i:m:o:")
	except getopt.GetoptError:
		print('RNN.py -i <dataDirName> -m <modelToUse> -o <modelSaveName>')
		sys.exit(2)
	saveName = dt.datetime.now().strftime("Model_%Y%m%d%H%M.h5")
	model = None
	for opt, arg in opts:
		if opt == '-i':
			dataDirName = arg
		elif opt == '-o':
			saveName = arg
		elif opt == '-m':
			#model = load_model(arg)
			model.load_weights(arg)
	if model == None:
		model = getModel(batch_size)
	useModel(model,saveName,dataDirName)

if __name__ == "__main__":
	main(sys.argv[1:])
