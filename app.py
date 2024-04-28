from flask import Flask, render_template, request
import faiss
from index_client import IndexClient
app = Flask(__name__)

from answer_analyser import AnswerAnalyser
index = faiss.read_index("hackathon.index")
index_client = IndexClient()
index_client.set_index(index)
analyser = AnswerAnalyser(index_client)

@app.route('/')
def index():
    return render_template('index.html')

BLANK_ANSWER_TXT = 'Blank answer, no information.'
def determine_result(question, answer, analyser, answer_dict):
    if answer == "":
        result = BLANK_ANSWER_TXT
        result_string = BLANK_ANSWER_TXT
    else:
        question_is_valid, result_string = analyser.analyse_answer(question, answer)
        result = answer_dict[question_is_valid]
    return result, result_string

@app.route('/submit', methods=['POST'])
def submit():
    question1 = 'We are collecting suggestions for a study on the subject of vacations. How would you describe your perfect vacation?'
    question2 = 'Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you?'
    question3 = 'Music has been called the greatest human creation throughout history. What role does Music play in your life?'

    answer1 = request.form[question1]
    answer2 = request.form[question2]
    answer3 = request.form[question3]
    valid_answer_dict = {
        True: 'Valid answer',
        False: 'Invalid answer'
    }
    answer_of_questions = {

    'answer3': answer3,
    'answer2' :answer2,
    'answer1':answer1

    }
    
    result3 = 'invalid answer'
    result2 = 'invalid answer'
    result1 = 'invalid answer'

    if answer1 == "" and answer2 == "" and answer3 == "":
        valid_answers = {
            'is_valid_answer3' : result3,
            'is_valid_answer2' : result2,
            'is_valid_answer1' : result1
        }
        final_result = False
        return render_template('index.html', valid_answers=valid_answers, answers_of_questions=answer_of_questions, final_result=final_result)
    
    result3, result_string3 = determine_result(question3, answer3, analyser, valid_answer_dict)
    result2, result_string2 = determine_result(question2, answer2, analyser, valid_answer_dict)
    result1, result_string1 = determine_result(question1, answer1, analyser, valid_answer_dict)
    

    valid_answers = {
    'is_valid_answer3' : result3,
    'is_valid_answer2' : result2,
    'is_valid_answer1' : result1,
    'answer3_analysis': result_string3,
    'answer2_analysis': result_string2,
    'answer1_analysis': result_string1,
    }
    
    detailed_analysis = {
        'answer3_analysis': result_string3,
        'answer2_analysis': result_string2,
        'answer1_analysis': result_string1,
    }
    print(detailed_analysis)
    final_result = (result3 == "Valid answer" or result3 == BLANK_ANSWER_TXT) \
                and (result2 == "Valid answer" or result2 == BLANK_ANSWER_TXT) \
                and (result1 == "Valid answer" or result1 == BLANK_ANSWER_TXT) 
    final_result = valid_answer_dict[final_result]
    
    return render_template('index.html', valid_answers=valid_answers, answers_of_questions=answer_of_questions, final_result=final_result, detailed_analysis=detailed_analysis)



if __name__ == '__main__':
    app.run(debug=True)
