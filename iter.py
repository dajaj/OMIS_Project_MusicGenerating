import mido_encodage as me
import os

def splitChannels(midiName,midiSource):
	outDir = 'channels/' + midiSource
	if not os.path.exists(outDir):
	  os.makedirs(outDir)
	
	outDir = outDir + '/' + midiName[:-4]
	if not os.path.exists(outDir):
	  os.makedirs(outDir)
	
	midiFile = 'MIDI/' + midiSource + '/' + midiName
	
	channels,metas=me.parseMidi(midiFile)
	me.saveMidiList(channels,outDir+'/chan_')

def scanDir(path="./",directory,action):
	for file in os.listdir(directory):
		if os.path.isdir(file):
			scanDir(path+directory,file,action)
		else:
			globals()[action](path+directory+file)

def feedRNNwithMIDI(midiFile):
	try:
		channels,metas=me.parseMidi(midiFile)
		for channel in channels:
			feedRNNwithChannel(channel)
	except:
		os.remove(midiFile)
		print(midiFile+" REMOVED")

def feedRNNwithChannel(channel):
	print("feeding")


if __name__ == "__main__":
	for sourceDir in os.listdir('MIDI'):
		print(sourceDir)
		for midiFile in os.listdir('MIDI/'+sourceDir):
			if not os.path.exists('channels/'+sourceDir+'/'+midiFile[:-4]):
				print('    '+midiFile)
				try:
					splitChannels(midiFile,sourceDir)
				except:
					os.remove('MIDI/'+sourceDir+'/'+midiFile)
					os.rmdir('channels/'+sourceDir+'/'+midiFile[:-4])
					print('      --> REMOVED')