from keras.layers.embeddings import Embedding
from recurrentshop import LSTMCell, RecurrentContainer
from seq2seq.cells import LSTMDecoderCell
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, TimeDistributed, Input
from keras.engine.topology import Layer
from keras import backend as K
import numpy as np

def getModel(batch_size):
	model = Sequential()
	model.add(Embedding(input_dim=128,output_dim=128))
	model.add(Seq2Seq(input_dim=128,output_dim=128,output_length=batch_size,hidden_dim=128))
	return model

# Taken from seq2seq and adapted
# Waiting to know if we add the ClassifierLayer
def Seq2Seq(output_dim, output_length, hidden_dim=None, depth=1, peek=False, dropout=0., **kwargs):
	if type(depth) == int:
		depth = [depth, depth]
	if 'batch_input_shape' in kwargs:
		shape = kwargs['batch_input_shape']
		del kwargs['batch_input_shape']
	elif 'input_shape' in kwargs:
		shape = (None,) + tuple(kwargs['input_shape'])
		del kwargs['input_shape']
	elif 'input_dim' in kwargs:
		if 'input_length' in kwargs:
			shape = (None, kwargs['input_length'], kwargs['input_dim'])
			del kwargs['input_length']
		else:
			shape = (None, None, kwargs['input_dim'])
		del kwargs['input_dim']
	if 'unroll' in kwargs:
		unroll = kwargs['unroll']
		del kwargs['unroll']
	else:
		unroll = False
	if 'stateful' in kwargs:
		stateful = kwargs['stateful']
		del kwargs['stateful']
	else:
		stateful = False
	if not hidden_dim:
		hidden_dim = output_dim
	
	encoder = RecurrentContainer(readout=True, state_sync=True, input_length=shape[1], unroll=unroll, stateful=stateful, return_states=True)
	for i in range(depth[0]):
		encoder.add(LSTMCell(hidden_dim, batch_input_shape=(shape[0], hidden_dim), **kwargs))
		encoder.add(Dropout(dropout))
	
	dense1 = TimeDistributed(Dense(hidden_dim))
	dense1.supports_masking = True
	
	dense2 = Dense(output_dim)
	
	decoder = RecurrentContainer(readout='add' if peek else 'readout_only', state_sync=True, output_length=output_length, unroll=unroll, stateful=stateful, decode=True, input_length=shape[1])
	for i in range(depth[1]):
		decoder.add(Dropout(dropout, batch_input_shape=(shape[0], output_dim)))
		decoder.add(LSTMDecoderCell(output_dim=output_dim, hidden_dim=hidden_dim, batch_input_shape=(shape[0], output_dim), **kwargs))
	decoder.add(Dense(output_dim,activation='softmax'))
	
	input = Input(batch_shape=shape)
	input._keras_history[0].supports_masking = True
	encoded_seq = dense1(input)
	encoded_seq = encoder(encoded_seq)
	encoded_seq = encoded_seq[-2:]
	
	wrapped_encoder = Model(input,encoded_seq)
	
	decoder_input = Input(batch_shape=(2,hidden_dim))
	decoder_input._keras_history[0].supports_masking = True
	states = decoder_input
	encoded_seq = decoder_input[-1]
	encoded_seq = dense2(encoded_seq)
	decoded_seq = decoder({'input': encoded_seq, 'initial_readout': encoded_seq, 'states': states})
	wrapped_decoder = Model(decoder_input,decoded_seq)
	
	decoded_seq = wrapped_decoder(wrapped_encoder)
	
	model = Model(input, decoded_seq)
	
	model.encoder = wrapped_encoder
	model.decoder = wrapped_decoder
	return model
