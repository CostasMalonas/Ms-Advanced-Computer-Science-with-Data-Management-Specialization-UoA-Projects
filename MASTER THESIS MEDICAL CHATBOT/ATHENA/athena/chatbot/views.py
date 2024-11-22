from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from django.views.decorators.csrf import csrf_exempt
import string
from nltk.corpus import stopwords
from django.views.decorators.http import require_POST
from .distilbert_transformer import get_answer
from django.shortcuts import render
import os
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

def load_landing_page(request):
    return render(request, 'chatbot/landing.html')




os.environ["OPENAI_API_KEY"] = 'your key' 

file_path = 'chatbot/formatted_data.txt'
loader = TextLoader(file_path=file_path)
index = VectorstoreIndexCreator().from_loaders([loader])
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 5}),
)

def chat_view(request):
    # Initialize chat history from session or start a new one if it doesn't exist
    chat_history = request.session.get('chat_history', [])
    
    # Check if it's a new chat session and prepend the initial chatbot message
    if not chat_history:
        initial_message = "Hello, I am Athena, your personal medical ChatBot. You can ask me any question of medical nature, and I will try to assist you the best I can. Please keep in mind that I am not a diagnosis tool and you should always consult medical professionals."
        chat_history.append({'user': '', 'bot': initial_message})
        request.session['chat_history'] = chat_history
    
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chain_history = [(item['user'], item['bot']) for item in chat_history if item['user']] 
        result = chain.run({"question": user_input, "chat_history": chain_history})  # Assuming chat_history used here is different from the session chat_history
        print(result)
        
        # Update chat history with the new user input and bot response
        chat_history.append({'user': user_input, 'bot': result})
        
        # Save the updated chat history back to the session
        request.session['chat_history'] = chat_history

    context = {'chat_history': chat_history}
    return render(request, "chatbot/chatbot.html", context)

def load_search_page(request):
    """
    Load the list of symptoms from the 'condition_symptoms' data file and send it to the frontend.

    This function reads the 'condition_symptoms' file which contains a mapping of conditions to their associated symptoms.
    It then flattens and consolidates the symptom lists, removes duplicates, and sorts them.
    The sorted list of unique symptoms is sent to the frontend to be displayed alongside the chatbox for user selection.

    Returns:
        render: Renders the 'search.html' template, passing the sorted list of symptoms to be used in the frontend.
    """
    global selected_symptoms
    selected_symptoms = []

    with open('condition_symptoms.json', 'r') as f:
        data = json.load(f)
    
    all_symptoms = [item for sublist in data.values() for item in sublist]
    unique_symptoms = list(set(all_symptoms))
    sorted_symptoms = sorted(unique_symptoms)

    return render(request, 'chatbot/search.html', {'symptoms': sorted_symptoms})






stop_words = set(stopwords.words('english'))
    
def search_symptoms(request):
    translator = str.maketrans('', '', string.punctuation)

    # remove punctuation and convert to lower case
    query = request.GET.get('q', '').translate(translator).strip().lower()
    query_words = [word for word in query.split() if word not in stop_words]


    isPsychological = request.GET.get('isPsychological', 'All')
    ageGroup = request.GET.get('ageGroup', 'ALL_AGES')
    gender = request.GET.get('gender', 'ALL_GENDERS')
    categories = request.GET.getlist('categories')  # Get categories from request
    categories = categories[0].strip().split(',') # With that line the user can select more than one categories
    print("Categories received:", categories)
    with open('transformed_condition_data.json', 'r') as f:
        data = json.load(f)

    symptom_set = set()
    symptom_match_counts = []

    for condition, condition_data in data.items():
        condition_categories = condition_data.get("Category", [])

        # Check if any of the selected categories are in the condition's categories
        if categories and not any(cat in condition_categories for cat in categories):
            continue


        if (isPsychological != 'All' and condition_data["Psychological"] != isPsychological) or \
           (condition_data["Age_Group"] != ageGroup and condition_data["Age_Group"] != "ALL_AGES") or \
           (condition_data["Gender"] != gender and condition_data["Gender"] != "ALL_GENDERS"):
            continue


        for symptom in condition_data["Symptoms"]:
            if symptom not in symptom_set:
                symptom_set.add(symptom)
                matched_words_count = sum(
                    1 for word in query_words if any(
                        symp_word.translate(translator).lower().startswith(word)
                        for symp_word in symptom.strip().split()
                    )
                )
                if matched_words_count > 0:
                    symptom_match_counts.append((symptom, matched_words_count))

    # Determine which symptoms to return
    if query:
        sorted_symptoms = sorted(
            (symptom for symptom, count in symptom_match_counts if count > 0),
            key=lambda x: x[0]
        )
    else:
        sorted_symptoms = sorted(symptom_set)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"symptoms": sorted_symptoms})

    return render(request, 'chatbot/search.html', {'symptoms': sorted_symptoms, 'query': query})




# Use a global variable to store the symptoms. (I will change that in the future)
selected_symptoms = []

@csrf_exempt
def store_symptoms(request):
    """
    Handle POST requests to store selected symptoms.

    When the user selects a symptom from the frontend, this function is called
    to update a global list of selected symptoms. This ensures that the user's 
    selected symptoms are accumulated and can be displayed in the chatbox. 
    Only unique symptoms are added, avoiding duplicates.

    Returns:
        JsonResponse: If the request is a POST, it returns the updated list of symptoms.
                      Otherwise, it returns an error indicating an invalid request method.
    """
    global selected_symptoms
    if request.method == "POST":
        new_symptoms = json.loads(request.body).get('Symptoms', [])
        
        # Append the new symptoms to the global list, avoiding duplicates
        for symptom in new_symptoms:
            if symptom not in selected_symptoms:
                selected_symptoms.append(symptom)
                
        return JsonResponse({"Symptoms": selected_symptoms})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



@require_POST
@csrf_exempt
def get_conditions(request):
    """
    Handle POST requests to retrieve potential health conditions based on selected symptoms.

    This view is called when the user clicks on the search button after selecting his symptoms.
    The function fetches the user's age from the request and determines the appropriate age group.
    It then matches the selected symptoms against the conditions to identify potential matches.
    The conditions are filtered based on the age group and symptoms.

    Returns:
        JsonResponse: A list of potential conditions based on the user's selected symptoms.
                      If there's an error reading the conditions data, an error message is returned.
    """
    global selected_symptoms
    selected_symptoms_local = selected_symptoms
    print('SELECTED SYMPTOMS LOCAL: ', selected_symptoms_local)
    selected_symptoms = []
    body = json.loads(request.body.decode('utf-8'))
    age = body.get('age', None)
    gender = body.get('gender', None)

    if age:
        ageGroup = age
    else:
        ageGroup = 'ALL_AGES'

    # Logic to match symptoms with conditions
    matching_conditions = []
    try:
        with open('transformed_condition_data.json', 'r') as data_file:
            conditions_data = json.load(data_file)
            for condition, condition_data in conditions_data.items():
                condition_symptoms = [symptom.lower().strip() for symptom in condition_data.get("Symptoms", [])]
                condition_age_group = condition_data.get('Age_Group', 'ALL_AGES')
                condition_gender_group = condition_data.get('Gender', 'ALL_GENDERS')
                # Check if any symptom matches
                if any(symptom.lower().strip() in condition_symptoms for symptom in selected_symptoms_local):
                    # Check if age group matches
                    if (condition_age_group.strip() == ageGroup.strip()) or (condition_age_group == 'ALL_AGES'):
                        # Check if gender group matches
                        if condition_gender_group.strip() == gender.strip() or condition_gender_group == 'ALL_GENDERS':
                            matching_conditions.append({
                                'name': condition,
                                'questions': condition_data.get('Questions', [])
                            })


    except (IOError, json.JSONDecodeError):
        return JsonResponse({"error": "Failed to load conditions data"}, status=500)

    return JsonResponse({"conditions": list(matching_conditions)})



def show_categories(request):
    with open('transformed_condition_data.json', 'r') as f:
        data = json.load(f)

    categories = sorted(set(cat for condition_data in data.values() for cat in condition_data.get("Category", [])))
    return JsonResponse({'categories': categories})


def search_categories(request):
    query = request.GET.get('q', '').lower().strip()
    try:
        with open('transformed_condition_data.json', 'r') as file:
            data = json.load(file)
        
        # Extract unique categories and filter based on the query
        all_categories = set()
        for condition_data in data.values():
            all_categories.update(condition_data.get("Category", []))

        filtered_categories = [cat for cat in all_categories if query in cat.lower()]

        return JsonResponse({"categories": filtered_categories})
    except IOError:
        return JsonResponse({"error": "Failed to load category data"}, status=500)
    

@csrf_exempt
def get_answer_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')
        condition = data.get('condition')
        # Use transformer to get the answer
        answer = get_answer(question, condition)
        return JsonResponse({'answer': answer})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)