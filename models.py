from seq2seq.models import SimpleSeq2Seq
from keras.models import Sequential
from keras.layers.embeddings import Embedding

def getModel(batch_size):
	model = Sequential()
	model.add(Embedding(input_dim=128,output_dim=128))
	model.add(SimpleSeq2Seq(input_dim=128,output_dim=128,output_length=batch_size))
	return model
