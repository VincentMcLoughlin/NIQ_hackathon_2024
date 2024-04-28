from index_client import IndexClient
from sentence_transformers import util
import fasttext
import requests
import deepl
from pprint import pprint

class AnswerAnalyser:
    
    def __init__(self, index_client=None, model_name="all-MiniLM-L6-v2", fasttext_model_path="lid.176.ftz"):
        if index_client:
            self.index_client = index_client
        else:
            self.index_client = IndexClient(model_name)
        
        self.lang_predict_model = fasttext.load_model(fasttext_model_path)
        self.min_semantic_similarity = 0.5
        self.max_semantic_similarity = 0.8
        self.duplicate_ans_distance = 0.00001
        
        deepl_auth_key = "c3b37c8f-07a9-421d-b9a5-7c20f7e6a115:fx"
        self.translator = deepl.Translator(deepl_auth_key)
        self.sapling_api_key = "5WEN0QAMKM5Q1JF86IRUKJUXKBI1N5H5"
        
    def analyse_answer(self, input_question, answer):
        input_question = str(input_question)
        answer = str(answer)
        
        is_same_language = self.is_same_language(input_question, answer)
        is_original_answer = self.is_original_answer(answer)
        is_human_language, probability_ai_answer = self.is_human_answer(answer)
        is_good_answer = self.is_good_answer(input_question, answer)
        
        result_string = f"<b>Same language:</b> {is_same_language}, <br><b>Original Answer:</b> {is_original_answer}, <br><b>Human Generated (% Chance of AI):</b> {is_human_language} ({probability_ai_answer}%), <br><b>Good Quality:</b> {is_good_answer}"        
        result = is_same_language and is_original_answer and is_human_language and is_good_answer
        
        return result, result_string
    
    def is_same_language(self, survey_question: str, input_sentence: str):
        is_same_language = False
        #lang_predict_model is a fasttext deep neural network for identifying languages
        survey_question_lang = self.lang_predict_model.predict(survey_question, k=1)[0][0].split('__label__')[1]        
        input_sentence_lang = self.lang_predict_model.predict(input_sentence, k=1)[0][0].split('__label__')[1]
        print(f"survey lang: {survey_question_lang} input_lang: {input_sentence_lang}")
        if input_sentence_lang == survey_question_lang:
            is_same_language = True

        return is_same_language
    
    def is_original_answer(self, answer: str):
        is_original_answer = True
        distance_df = self.index_client.find_nearest_neighbours(answer)
        closest_distance = distance_df['distance'].loc[0]

        if closest_distance < self.duplicate_ans_distance:
            is_original_answer = False
        else:
            self.index_client.add_text_to_index(answer)

        return is_original_answer
    
    def is_human_answer(self, input_sentence):
        # Use Sapling and DeepL
        is_human_answer = True
        
        # Check if the input sentence is in English, if not translate it to English. Sapling does not work well for non-english answers
        if self.lang_predict_model.predict(input_sentence, k=1)[0][0].split('__label__')[1] != "en": 
            input_sentence = self.translator.translate_text(input_sentence, target_lang="EN-US").text
        
        # Sapling is able to detect AI generated answers, even if generated in another language as well as non-translated
        # From our testing, translating human generated answers does not substantially change the detection result.
        response = requests.post(
            "https://api.sapling.ai/api/v1/aidetect",
            json={
                "key": self.sapling_api_key,
                "text": input_sentence
            }
        )
        pprint(response.json())
        
        if 'score' not in response.json(): #Occasionally the API returns an error, in this case we assume the answer is human generated
            return is_human_answer
        
        probability_ai_answer = response.json()['score']
        print(f"AI Probability: {probability_ai_answer}")
        if probability_ai_answer > 0.99: #Sapling has a ton of false positives, particularly for short sentences
            is_human_answer = False
        
        probability_ai_answer = round(probability_ai_answer*100, 2)
        return is_human_answer, probability_ai_answer, 
    
    def is_good_answer(self, survey_question: str, input_sentence: str):
        is_good_answer = False
        question_embeddings = self.index_client.embedder.encode([survey_question], convert_to_tensor=True)
        answer_embeddings = self.index_client.embedder.encode([input_sentence], convert_to_tensor=True)
        
        cosine_scores = util.cos_sim(question_embeddings, answer_embeddings)
        
        if float(cosine_scores[0][0]) > self.min_semantic_similarity and float(cosine_scores[0][0]) < self.max_semantic_similarity:
            is_good_answer = True
        print(f"SIMILARITY: {cosine_scores[0][0]}")
        return is_good_answer
    
