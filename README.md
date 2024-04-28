# NIQ Hackathon 2024 Challenge #1

Team Name: Mind Benders

Team Members:
Chennapan Radhakrishnan
Luis Alberto Munoz
Vincent McLoughlin

# Overview 

Online surveys can be a very useful tool for gathering data. It is quite typical for organizations to put out surveys, and offer rewards in the forms of coupons or vouchers to encourage people to respond. Unfortunately, getting quality answers to questions can be a real challenge, as bad quality answers, click farm response, incoherent answers and other bad answers are very common repsonses to these surveys. For our hackathon challenge, we were expected to detect bad answers from a set of three questions. These questions were the following:

- We are collecting suggestions for a study on the subject of vacations. How would you describe your perfect vacation?


- Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you?


- Music has been called the greatest human creation throughout history. What role does Music play in your life?


These questions could be asked or answered in any one of five languages, English, German, French, Spanish, or Italian.

# Bad Quality Criteria
The organizers provided the following criteria for judging whether and answer was bad quality or not. 

* Nonsense 
* Bad language
* Generic answer
* Wrong language
* Wrong topic, answer does not fit to question
* Duplicate answers within respondent
* Duplicate answers across respondents
* AI generated answers
* AI translated answers
* Copy pasted answers


# The Data

The data for this challenge took the form of an excel document where each row represented a set of respondent answers. The excel file contains 4403 entries. Respondents could be asked at most two of the three possible questions, but they only had to answer one. Therefore empty answers are not necessarily bad quality. According to the organizers, our dataset contains real valid answers, real bad quality data and made-up bad quality data. Some example answers can be seen in the table below.

|Question 1                                                                                                 |Question 2                                        |Question 3                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Anywhere that I can escape from the world. Easy of getting there and ability to do it at a reasonable cost.|                                                  |I listen to music nearly all day during working.                                                                                                                                  |
|Boaboa                                                                                                     |Tonka                                             |                                                                                                                                                                                  |
|Eine gemütliche Hütte im Wald, weit weg vom Trubel, für einen ruhigen und abgeschiedenen Urlaub.           |                                                  |Musik ist mein Motivator und meine Muse. Sie beflügelt meine Kreativität und macht alltägliche Aufgaben angenehmer, indem sie Momente der Innovation und Introspektion inspiriert.|
|frdhfgjghkjgl                                                                                              |sdgjhgsfhdsh                                      |                                                                                                                                                                                  |
|Gemütliches Hotel zum wohlfühlen. Gute Verpflegung, geschultes Personal, Ausflugsmöglichkeiten             |Ball - vielseitig, allein und mit anderen spielbar|                                                                                                                                                                                  |
|Sitting my ass in the sand , relaxing drinking booze and not a care in the world                           |                                                  |                                                                                                                                                                                  |


A few things to note about the data:

* The data is unlabelled, so supervised learning algorithms (such as deep neural networks) are not a great candidate for our solution.
* The unlabelled data means we have no way of knowing which are AI generated or not. 
* Answers tend to be short, on average less than 100 characters, and none longer than a couple of sentences.
* Some answers contain bad language, but are still valid answers, for example, the last entry in our example so any profanity filtering here would need to be careful.
* Our data is in multiple languages, so any solution must be flexible enough to deal with this. 

# Our solution
From our three team members, I had the most experience with data science, so it was decided that I would handle our backend/modeling, Luis would handle our front end, and Chennapan would assist both us depending on what needed work.

## Primary Quality Criteria

We decided to focus on four key areas as we felt that would provide us the best detection coverage given the criteria we received from the organizers:

* Is the answer the same languageas the input question?
* Is the answer original?
* Is the answer human generated?
* Is our answer a good, on-topic answer?

Answering these four questions would allow us to cover all of the criteria provided by the organizers, with the exception of the copy-pasted answer criterion. There was no way to detect if an answer was copy and pasted from the data provided in our excel sheet this, plus this would be a relatively easy issue to address with some front end logic to prevent user's from copy and pasting, so we did not focus on that criterion. All other criteria are covered by these four. 

## Criteria 1: Is our answer the same language as the input question?
For determining if our answer was the same language as the input question, we use a fasttext deep neural network model for determining if our answer language and our question language are the same. This is a simple equality check, so if the languages are different, we reject the answer. 

## Is the answer original?
Next we want to determine if an answer is a duplicate answer or not. To accomplish this we use a simple vector database called FAISS. FAISS is a realtively lightweight vector store that comes with all the features you would need for a simple vector database. Most importantly, it all can run locally, meaning it is a good fit for a simple project like ours. For each submitted answer, we convert our answer into vector embeddings that allow us to numerically represent our answers. We then check if the answer is already present in our FAISS database. If it is, we reject the answer. If not, we add the response to our vector database so we can detect if the response is resubmitted in future. 

## Is the answer human generated?

## Is our answer a good on-topic answer?

# Old readme

This is the submission for challenge #1 of the NIQ Hackathon. It consists of two ways to run our analysis. The first is to run the app.py file, which will deploy a local website where the user can test different input combinations.

The second is by using the analyse_file.py script. This file will read Data\hackfest_20231127.xlsx and analyse each answer. It will add three colummns for the result of each response for each row, and another three columns containing the reason why a specific answer may have passed/failed. An overall result column is also included.

The main logic is contained in the answer_analyser.py file. Our four functions for analysing an answers quality can be found there.

