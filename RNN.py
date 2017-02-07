from preprocess import preprocessMidi
from models import getModel
from sklearn.model_selection import train_test_split
import numpy as np
import sys,getopt
import datetime as dt

output_length = 20
dataDirName = "MIDI/test"

def importDataSet(dirName):
	print(":: IMPORTING DATA SET")
	X,y = preprocessMidi(dirName,verbose=0,removeExceptions=True,
							max_sample_len=output_length,
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
	model.fit(X,y,batch_size=1,nb_epoch=5,validation_split=0.4)

def evalModel(model,X,y):
	print(":: EVALUATING MODEL ON TEST DATA")
	metrics = model.evaluate(X,y,batch_size=1)
	for i in range(len(metrics)):
		print(model.metrics_names[i]+" : "+str(metrics[i]))

def useModel(model,modelSaveName,dataDir):
	X_train,X_test,y_train,y_test = importDataSet(dataDir)
	compileModel(model)
	for i in range(30):
		print("~~ ROUND "+str(i))
		fitModel(model,X_train,y_train)
		evalModel(model,X_test,y_test)
	model.save_weights(modelSaveName)

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"i:w:o:")
	except getopt.GetoptError:
		print('RNN.py -i <dataDirName> [-w <weightsToUse>] [-o <modelSaveName>]')
		sys.exit(2)
	saveName = dt.datetime.now().strftime("Weights_%Y%m%d%H%M.h5")
	model = getModel(output_length)
	for opt, arg in opts:
		if opt == '-i':
			dataDirName = arg
		elif opt == '-o':
			saveName = arg
		elif opt == '-w':
			model.load_weights(arg)
	useModel(model,saveName,dataDirName)

if __name__ == "__main__":
	main(sys.argv[1:])
