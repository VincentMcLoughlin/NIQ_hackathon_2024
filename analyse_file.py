import faiss
from index_client import IndexClient
from answer_analyser import AnswerAnalyser
import pandas as pd

BLANK_ANSWER_TXT = 'Blank answer, no information.'

def analyse_row(row, index, analyser, q1_results, q2_results, q3_results, q1_detailed_analyses, q2_detailed_analyses, q3_detailed_analyses, overall_results):
    
    q1= "We are collecting suggestions for a study on the subject of vacations. \
        How would you describe your perfect vacation?"
        
    q2="Childhood memories are always special, and toys play an important role \
        in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you?"
    
    q3 = "Music has been called the greatest human creation throughout history. What role does Music play in your life?"
    
    # if row["qcheck"] == "" and row["x01_2"] == "" and row["x01_3"] == "":
    #     q1_is_valid_answer = False
    #     q2_is_valid_answer = False        
    #     q3_is_valid_answer = False
    #     q1_detailed_analysis = BLANK_ANSWER_TXT
    #     q2_detailed_analysis = BLANK_ANSWER_TXT
    #     q3_detailed_analysis = BLANK_ANSWER_TXT
    #     overall_result = False
        
    #     q1_results[index] = q1_is_valid_answer
    #     q2_results[index] = q2_is_valid_answer
    #     q3_results[index] = q3_is_valid_answer
    #     q1_detailed_analyses[index] = q1_detailed_analysis 
    #     q2_detailed_analyses[index] = q2_detailed_analysis 
    #     q3_detailed_analyses[index] = q3_detailed_analysis 
    #     overall_results[index] = overall_result        
    #     return
    
    # Can't assume empty answer is bad quality, if one has text, then use that to determine
    if row["qcheck"] == "":
        q1_is_valid_answer = True
        q1_detailed_analysis = BLANK_ANSWER_TXT
    else:
        q1_is_valid_answer, q1_detailed_analysis = analyser.analyse_answer(q1, row["qcheck"])
        
    # if row["x01_2"] == "":
    #     q2_is_valid_answer = True
    #     q2_detailed_analysis = BLANK_ANSWER_TXT
    # else:
    #     q2_is_valid_answer, q2_detailed_analysis = analyser.analyse_answer(q2, row["x01_2"])    
    
    # if row["x01_3"] == "":
    #     q3_is_valid_answer = True
    #     q3_detailed_analysis = BLANK_ANSWER_TXT
    # else:
    #     q3_is_valid_answer, q3_detailed_analysis = analyser.analyse_answer(q3, row["x01_3"])
    
    # If any bad quality answers, flag as invalid
    #overall_result = q1_is_valid_answer and q2_is_valid_answer and q3_is_valid_answer
    q1_results[index] = q1_is_valid_answer
    #q2_results[index] = q2_is_valid_answer
    #q3_results[index] = q3_is_valid_answer
    q1_detailed_analyses[index] = q1_detailed_analysis 
    #q2_detailed_analyses[index] = q2_detailed_analysis 
    #q3_detailed_analyses[index] = q3_detailed_analysis 
    #overall_results[index] = overall_result           

def main():
    input_file = "Data\hackfest_20231127.xlsx"
    #input_file = "Data\wehack_subset.xlsx"
    index_client = IndexClient()
    index_client.add_text_to_index("Example text") #Need at least one entry for comparisons
    analyser = AnswerAnalyser(index_client)
    analyser.min_semantic_similarity = 0.33
    analyser.max_semantic_similarity = 0.8
    data_df = pd.read_excel(input_file).fillna("")
    num_entries = data_df.shape[0]
    q1_results = ['']*num_entries
    q2_results = ['']*num_entries
    q3_results = ['']*num_entries
    q1_detailed_analyses = ['']*num_entries
    q2_detailed_analyses = ['']*num_entries
    q3_detailed_analyses = ['']*num_entries
    overall_results = ['']*num_entries
    for i in range(data_df.shape[0]):
        row = data_df.iloc[i]        
        try:
            if i%50 == 0:
                print(f"Current index: {i}")
            analyse_row(row, i, analyser, q1_results, q2_results, q3_results, q1_detailed_analyses, q2_detailed_analyses, q3_detailed_analyses, overall_results)
        except Exception as e:
            print(f"ERROR: STOPPING PROCESSING")
            raise(e)
        finally:
            data_df['q1_results'] = q1_results
            #data_df['q2_results'] = q2_results
            #data_df['q3_results'] = q3_results
            data_df['q1_detailed_analysis'] = q1_detailed_analyses
            #data_df['q2_detailed_analysis'] = q2_detailed_analyses
            #data_df['q3_detailed_analysis'] = q3_detailed_analyses
            #data_df['overall_result'] = overall_results
            data_df.to_csv("output.csv", index=False)
    
if __name__ == "__main__":
    main()