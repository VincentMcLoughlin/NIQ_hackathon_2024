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

## Criteria 2: Is the answer original?
Next we want to determine if an answer is a duplicate answer or not. To accomplish this we use a simple vector database called FAISS. FAISS is a realtively lightweight vector store that comes with all the features you would need for a simple vector database. Most importantly, it all can run locally, meaning it is a good fit for a simple project like ours. For each submitted answer, we convert our answer into vector embeddings that allow us to numerically represent our answers. We then check if the answer is already present in our FAISS database. If it is, we reject the answer. If not, we add the response to our vector database so we can detect if the response is resubmitted in future. 

## Criteria 3: Is the answer human generated?
Detecting A.I generated text is still very much an open research question. Because of this, we decided to rely on a paid solution (with a free trial!) rather than trying to tackle it ourselves in the time that we had. There are a variety of services that attempt to solve this problem, but we spent the most time testing ZeroGPT, a popular A.I detection tool, RADAR, a solution produced by IBM, and Sapling, another paid service that seems to be popular online. We tested each of them, and unfortunately none of them were particularly good. Each of them noted that short strings were more difficult to perform checks on, which makes our case particularly challenging. 

A popular method for detecting A.I text is checking how many words produced by the LLM are low-frequency words. LLMs are much less likely to use rarely-used words than human generated answers, and these services likely rely on something similar to their detection, although it is difficult to know this as the code is not open source.

For our solution, we decided to go with Sapling, as it was the best of the products we tested. It was very prone to false positives, so if Sapling was more than 99% that detect was A.I generated, only then did we reject an answer.

One final note, Sapling is only tuned for English, so we use a free trial of DeepL to translate our answers to english solely for the AI checking component. We tested some AI generated answers, generated by ChatGPT and found it worked equally well for both original English answers, and translated answers.

## Criteria 4: Is our answer a good on-topic answer?
This is also a bit of a tricky problem. We have no labels associated with our data so it we can't rely on something like a neural network or other supervised classification algorithms. We could classify the text ourselves, either manually or by using ChatGPT or something similar, but that would be time consuming in the case of the manual classification, or potentially inaccurate/expensive in the case of ChatGPT. 


To solve this, we decided to use semantic embeddings. We convert the question into its equivalent embedding vector, and do the same for the answer. We then get the cosine distance between the question vector and the answer vector, and if our question and answer are close, we say our answer is valid. This allows us to reject answers that have nothing but junk or profanity, but keep answers such as "Sitting on my ass on the beach" which does contain foul language, but is a valid answer to the vacation question.

We put in one more threshold. If our question and answer are too similar, it is possible someone copied and pasted the question into the answer to try and get around our minimum distance check. This allows us to reject answers where people are copying and pasting in the questions or part of the questions, and so ensures our accepted answers are good on-topic answers.

## Performance


## Overall Placement

Our solution placed in the top 3 of our hackathon, out of 11 submissions so the judges liked our solution. We did not receive specific feed back, but unfortunately, we lost out on top place to another team, who focused on a solution that rejected copy and pasted input. This is a good tactic to reject bot-farm or click farm input and so was valued more by the judges. Still, top 3 is quite a good placement and overall we were happy with our effort, and learned a lot through the project that we would not have otherwise.

## Running Our Code/A Note on Code Structure   

Our repo has two ways to run our analysis. The first is to run the app.py file, which will deploy a local website where the user can test different input combinations.

The second is by using the analyse_file.py script. This file will read Data\hackfest_20231127.xlsx and analyse each answer. It will add three colummns for the result of each response for each row, and another three columns containing the reason why a specific answer may have passed/failed. An overall result column is also included.

The main logic is contained in the answer_analyser.py file. Our four functions for analysing an answers quality can be found there.

It is recommended to create a virtual environment and install our requirements file in requirements.txt. 

