# Introduction

This is the KBQA (Knowledge Graph-Driven Question Answering) project program - a lightweight QA system that matches
user-input questions to templates, queries the knowledge base for results, and generates summaries.

## Environment

python 3.9

## Install (online)

### Switch to the project directory

pip install -r requirements.txt

## Start

python query.py

## Project Structure

---- entityextraction(folder): Entity extraction algorithm for question statements

--------model(folder): Trained named entity recognition model

--------crf.py: Algorithm module

--------data.py: Data import module

--------predict.py: Prediction module

--------train.py: Training module

---- templatematching(folder): Template matching module

--------top5.py: Template matching algorithm based on SentenceTransformer model

---- generate_summary_test.py: Answer result generation function

---- main.py: System main module, starts and links each module

---- query.py: Links to the graph database for querying

## Process

### 1. Start the Neo4j Graph Database

1.1 For Community Edition: Open the terminal via Win+R, then type 'neo4j start' to initiate the database.

1.2 For Desktop Edition: Directly click the icon, run the corresponding project file, and open the data.

### 2. Execute main.py

After launching main.py, enter your question when prompted with 'Enter question (type "esc" to exit)', and wait for the
program to run and return the corresponding answers to geological questions.

### 3. Operational Principle

Upon inputting a question, the "user_question" variable is passed to both the template matching module and the entity
extraction module. The template matching module (templatematching) outputs the template most similar to the query,
stored in the (corpus) variable. The entity extraction module extracts relevant entities from the query, stored in
the (wordlist) variable. Both (corpus) and (wordlist) are then passed to the Database Query Module (query), which
outputs the corresponding results (result) to the Answer Generation Module for sequential output.

### 4. Example

![1.jpg](img%2F1.jpg)
![2.png](img%2F2.png)
![3.png](img%2F3.png)
![4.png](img%2F4.png)

## Paper

[A Knowledge Graph-Driven Question Answering System for Mineral Resource Survey](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5042985)
