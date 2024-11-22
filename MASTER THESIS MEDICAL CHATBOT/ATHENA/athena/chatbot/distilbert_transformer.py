from transformers import pipeline
import json
import time


def print_with_delay(text, delay=0.3):
    """Prints text with a delay between each character."""
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()

def select_relevant_context(question, condition_data, conditions_context):

    conditions_context_lower_dict = {key.lower():key for key in conditions_context}
    question_lower = question.lower()

    context_ls = []
    for key in conditions_context_lower_dict.keys():
        if key in question_lower:
            context_ls.append(key) 

    if len(context_ls) == 0:
        return context_ls, conditions_context_lower_dict
    
    return context_ls, conditions_context_lower_dict

def split_question(question):
    keywords = ['and', 'or', 'also', 'additionally']
    chunks = [question]
    for keyword in keywords:
        temp = []
        for chunk in chunks:
            temp.extend(chunk.split(keyword))
        chunks = temp
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def main():
    with open('question_answering.json', 'r') as file:
        data = json.load(file)

    qa = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad',  max_answer_length=10000)

    condition = input('For what condition do you want to get information? Atrial Fibrillation or Anorexia nervosa - Adults? Please type one of the two: ')

    if condition in data:
        conditions_context = data[condition]

        while True:
            question = input(f'What would you like to know about {condition}? (type "exit" to quit): ')
            
            if question.lower() == 'exit':
                break

            question_chunks = split_question(question)

            answer_final = ''
            for chunk in question_chunks:
                context_ls, conditions_context_lower_dict = select_relevant_context(chunk, conditions_context, conditions_context.keys())
                
                if len(context_ls) == 0:
                    answer_final += f'Sorry, I could not find an answer for: {chunk} Try to rephrase your question to include the words: {conditions_context.keys()}'
                else:
                    for word in context_ls:
                        context_text = conditions_context[conditions_context_lower_dict[word]]
                        answer = qa(context=context_text, question=chunk)
                        if answer['answer'] in context_text:
                            answer_final += '\n' + conditions_context_lower_dict[word] + ':\n' + context_text + '\n'
                        else:
                            answer_final += 'Sorry, I could not retrieve information for that matter...\n'


            print(answer_final)

    else:
        print_with_delay('Invalid condition')

qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad', max_answer_length=10000)

def get_answer(question, condition):
    """
    Generate an answer to the user's question based on the specified condition.

    Args:
    question (str): The user's question.
    condition (str): The health condition the question is about.

    Returns:
    str: The answer to the question.
    """
    try:
        with open('question_answering.json', 'r') as file:
            data = json.load(file)

        if condition not in data:
            return "Sorry, I don't have information about this condition."

        conditions_context = data[condition]

        question_chunks = split_question(question)

        answer_final = ''
        for chunk in question_chunks:
            context_ls, conditions_context_lower_dict = select_relevant_context(chunk, conditions_context, conditions_context.keys())

            if len(context_ls) == 0:
                answer_final += f'Sorry, I could not find an answer for: {chunk} Try to rephrase your question to include the words: {list(conditions_context.keys())}'
            else:
                for word in context_ls:
                    context_text = conditions_context[conditions_context_lower_dict[word]]
                    answer = qa_pipeline(context=context_text, question=chunk)

                    if answer['answer'] in context_text:
                        answer_final += conditions_context_lower_dict[word] + ':\n' + context_text + '\n'
                    else:
                        answer_final += 'Sorry, I could not retrieve information for that matter...\n'

        return answer_final

    except Exception as e:
        return f"An error occurred: {str(e)}"