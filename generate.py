from preprocess import addMidiToList,predict_sample,train_sample
from mido_encodage import vectList2midi,midiChannels2midi,saveMidi
from models import getModel
import numpy as np
import sys,getopt
import datetime as dt

def generateMIDI(MIDIinput,weights,saveName):
	model = getModel(20)
	model.load_weights(weights)
	MIDIlist = []
	addMidiToList(MIDIinput,MIDIlist,verbose=0)
	channels = []
	nb = 0
	for channel in MIDIlist:
		print("Channel "+str(nb))
		X = predict_sample([channel],max_sample_len=20)
		y = model.predict(X,batch_size=1,verbose=1)
		#X,y = train_sample([channel],max_sample_len=20)
		y = y.tolist()
		ch_list = []
		for batch in y:
			ch_list.extend(batch)
		ch_mid = vectList2midi(ch_list)
		channels.append(ch_mid)
		saveMidi(ch_mid,"ch"+str(nb)+".mid")
		nb+=1
	midi = midiChannels2midi(channels)
	saveMidi(midi,saveName)

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"i:w:o:")
	except getopt.GetoptError:
		print(usage())
		sys.exit(2)
	saveName = dt.datetime.now().strftime("GENERATED_%Y%m%d%H%M.mid")
	MIDIinput = None
	weights = None
	for opt, arg in opts:
		if opt == '-i':
			MIDIinput = arg
		elif opt == '-o':
			saveName = arg
		elif opt == '-w':
			weights = arg
	if MIDIinput == None or weights == None:
		raise Exception(usage())
	generateMIDI(MIDIinput,weights,saveName)

def usage():
	return 'RNN.py -i <MIDIinput> -w <weightsToUse> [-o <generatedMIDIname>]'

if __name__ == "__main__":
	main(sys.argv[1:])

