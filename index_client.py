# Ingest documents into vectorDB

from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import pandas as pd

class IndexClient:

  def __init__(self, sentence_transformer_model="all-MiniLM-L6-v2"): #"paraphrase-mpnet-base-v2"
    self.embedder = SentenceTransformer(sentence_transformer_model)
    vector_dimension = self.embedder.encode(["Example Text"]).shape[1] #Use to get vector, then get shape of output vector for our FAISS index
    self.index =faiss.IndexFlatL2(vector_dimension)
      
  def add_texts_to_index(self, input_data_df, text_column):    
    text = input_data_df[text_column].astype('str')
    print(f"Indexing {text_column}")
    vectors = self.embedder.encode(text)
    faiss.normalize_L2(vectors)
    self.index.add(vectors)
  
  def add_text_to_index(self, input_text):
    vectors = self.embedder.encode([input_text])
    faiss.normalize_L2(vectors)
    self.index.add(vectors)
    
  def set_index(self, index):
    self.index = index
  
  def find_nearest_neighbours(self, search_text):
    search_vector = self.embedder.encode(search_text)
    _vector = np.array([search_vector])
    faiss.normalize_L2(_vector)
    k = self.index.ntotal
    distances, ann = self.index.search(_vector, k=k)
    results = pd.DataFrame({'distance': distances[0], 'original_df_index': ann[0]})
    return results