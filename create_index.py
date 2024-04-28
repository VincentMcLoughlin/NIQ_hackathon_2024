from index_client import IndexClient
import faiss
import pandas as pd
input_data_df = pd.read_excel("Data/hackfest_20231127.xlsx")
index_client = IndexClient()
index_client.add_texts_to_index(input_data_df, text_column="x01_2")
index_client.add_texts_to_index(input_data_df, text_column="qcheck")
index_client.add_texts_to_index(input_data_df, text_column="x01_3")
faiss.write_index(index_client.index, "hackathon.index")