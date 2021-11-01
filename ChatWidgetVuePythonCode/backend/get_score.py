import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from word_data import word_data

with open("tokenizer.pkl", "rb") as file:
  tokenizer = pickle.load(file)

model = tf.keras.models.load_model("model.hdf5")

def get_positivity(sentences, types):
  sequences = tokenizer.texts_to_sequences(sentences)
  padded = pad_sequences(sequences, maxlen=200)
  ans = [i[2] for i in model.predict(padded)]
  similarity_score = [get_similarity(sentences[i], word_data[types[i]]) for i in range(2)]

  final_ans = []
  for i in range(2):
    if (ans[i]+similarity_score[i])*5 < 5:
      final_ans.append((ans[i]+similarity_score[i])*5)
    else:
      final_ans.append(5)
  
  marks_list={}
  for item in types:
    marks_list[item]=0.0

  sentences[0]=final_ans[0]
  sentences[1]=final_ans[1]
  for i in range(12):
    marks_list[types[i]]=marks_list[types[i]]+float(sentences[i])
    

  for item,value in marks_list.items():
    if(item in types[:2]):
      value=str(value/3.0)+"/5"
    else:
      value=str(value/2.0)+"/5"

  return marks_list

    


