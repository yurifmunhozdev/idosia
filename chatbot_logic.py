import nltk

# Attempt to download NLTK resources if not already present.
# The worker environment should ideally handle this, but it's good practice to include it.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError: # More general, but nltk.downloader.DownloadError was wrong
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError: # More general
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError: # More general
    nltk.download('omw-1.4', quiet=True)

try:
    # word_tokenize also uses 'punkt_tab' implicitly for some languages if not found.
    # It's better to ensure it's available.
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# --- Response Definitions ---
responses = {
    "greeting": "Hello! I am Idosia's health assistant. How can I help you today? You can ask me about common health markers, how to use this app, or general health tips.",
    "farewell": "You're welcome! Stay healthy and feel free to ask if you have more questions later.",
    "default": "I'm sorry, I can only provide information about health parameters tracked by Idosia and help you use the application. For other questions or medical advice, please consult a healthcare professional.",
    "blood_pressure_info": "Normal blood pressure is typically around 120/80 mmHg. High blood pressure might indicate an increased risk for cardiovascular problems. Idosia helps you track your readings. Remember to consult your doctor for medical advice.",
    "cholesterol_info": "An optimal LDL cholesterol level is generally below 100 mg/dL, but it depends on individual risk factors. High LDL can contribute to plaque buildup in arteries. Idosia can track your LDL levels. Please consult your doctor for personalized advice.",
    "glicemia_info": "Fasting blood glucose is typically normal if below 100 mg/dL. Levels between 100-125 mg/dL may indicate pre-diabetes, and above 126 mg/dL on two separate tests may indicate diabetes. Idosia helps track your glucose. A doctor can provide a diagnosis and guidance.",
    "creatinine_info": "Creatinine levels help assess kidney function. Typical ranges are about 0.6 to 1.2 mg/dL, but can vary. Higher levels might suggest impaired kidney function. Idosia allows you to note this value. Consult your doctor for interpretation.",
    "app_input_guidance": "You can enter your health data like age, cholesterol, blood pressure, glucose, and creatinine in the form on the main page. After submitting, you'll see your analysis and recommendations.",
    "app_dashboard_guidance": "The dashboard, when implemented with data storage, will show you trends in your health parameters over time. Currently, it visualizes your latest input alongside a sample historical point.",
    "health_tip_general": "For general well-being, maintaining a balanced diet, regular physical activity, and routine check-ups are important. For specific advice related to your health parameters, Idosia provides some suggestions after you input your data, and your doctor can give you the best guidance.",
    "health_tip_bp": "To help manage blood pressure, common advice includes reducing salt intake, regular exercise, and managing stress. Please discuss specific strategies with your doctor.",
}

# --- Keyword Definitions ---
keywords = {
    "greeting": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"],
    "farewell": ["bye", "thanks", "thank", "thankyou", "farewell", "see you", "appreciate it"],
    "blood_pressure": ["blood pressure", "bp", "pressure"],
    "cholesterol": ["cholesterol", "ldl"],
    "glicemia": ["glicemia", "glucose", "sugar"],
    "creatinine": ["creatinine", "kidney", "renal function"],
    "app_input": ["input", "enter", "data", "form", "add", "record"],
    "app_dashboard": ["dashboard", "history", "trends", "view data", "view history"],
    "app_usage": ["how to use", "app help", "application usage", "guide", "use this app"],
    "health_tips": ["tips", "advice", "help with", "suggest", "recommend", "health tips"],
    "lower_bp_tips": ["lower blood pressure", "reduce bp", "manage blood pressure", "lower my blood pressure"],
}


def get_chatbot_response(user_input: str) -> str:
    user_input_lower = user_input.lower()
    
    # Tokenize and lemmatize
    # For multi-word keywords, it's often better to check the raw lowercased input first,
    # or to process n-grams from the tokens.
    # For this version, we'll primarily use token matching and some direct string checks for multi-word keywords.
    
    tokens = nltk.word_tokenize(user_input_lower)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # --- Intent Matching ---

    # Order of checks can be important. More specific should come before general.

    # Specific Health Tips first
    if any(phrase in user_input_lower for phrase in keywords["lower_bp_tips"]):
        return responses["health_tip_bp"]

    # App Usage Guidance - These specific phrases should be checked BEFORE greetings
    if "how to use this app" in user_input_lower or \
       any(phrase in user_input_lower for phrase in keywords["app_usage"] if phrase == "how to use this app"): # Ensure exact match from keywords
         return responses["app_input_guidance"] 
    if "view history" in user_input_lower or \
       any(phrase in user_input_lower for phrase in keywords["app_dashboard"] if phrase == "view history"):  # Ensure exact match from keywords
        return responses["app_dashboard_guidance"]

    # Farewell (check early as "thanks" can be in other contexts)
    if any(keyword in user_input_lower for keyword in keywords["farewell"]): 
        if not any(neg_kw in user_input_lower for neg_kw in ["not thank", "no thanks"]):
             return responses["farewell"]
    
    # Greeting - Should come after specific app usage questions that might contain common words
    if any(keyword in user_input_lower for keyword in keywords["greeting"]):
        return responses["greeting"]

    # Health Parameter Info
    if any(phrase in user_input_lower for phrase in ["blood pressure", "my bp"]):
        return responses["blood_pressure_info"]
    if "cholesterol" in lemmatized_tokens or "ldl" in lemmatized_tokens:
        return responses["cholesterol_info"]
    if "glicemia" in lemmatized_tokens or "glucose" in lemmatized_tokens or "sugar" in lemmatized_tokens:
        return responses["glicemia_info"]
    if "creatinine" in lemmatized_tokens or any(kw in lemmatized_tokens for kw in ["kidney", "renal"]):
        return responses["creatinine_info"]
    
    # More general App Usage Guidance 
    if any(phrase in user_input_lower for phrase in ["show dashboard"] + keywords["app_dashboard"]):
        return responses["app_dashboard_guidance"]
    if any(phrase in user_input_lower for phrase in ["how to input", "enter data", "fill form"] + keywords["app_input"]):
        return responses["app_input_guidance"]
    # Check lemmatized tokens for general app keywords if specific phrases didn't match
    # This might be redundant if keywords["app_input"] and keywords["app_dashboard"] are already checked above with user_input_lower
    if any(keyword in lemmatized_tokens for keyword in keywords["app_input"]):
        return responses["app_input_guidance"]
    if any(keyword in lemmatized_tokens for keyword in keywords["app_dashboard"]):
        return responses["app_dashboard_guidance"]
        
    # General Health Tips (after specific parameter info and app usage)
    if any(keyword in user_input_lower for keyword in keywords["health_tips"]) or \
       any(token in lemmatized_tokens for token in ["tip", "advice", "suggest", "recommend"]): # "health tips" was added to keywords["health_tips"]
        return responses["health_tip_general"]


    # Default response if no specific intent is matched
    return responses["default"]

if __name__ == '__main__':
    print("Idosia Chatbot Test Mode:")
    print("-------------------------")
    
    test_inputs = [
        "Hello there",
        "hey",
        "What is normal blood pressure?",
        "tell me about my bp",
        "cholesterol levels",
        "ldl",
        "What about glicemia?",
        "glucose",
        "creatinine meaning",
        "kidney function",
        "How to input data?",
        "how do I enter my numbers",
        "show me the dashboard",
        "view history",
        "how to use this app",
        "any health tips?",
        "how can I lower blood pressure?",
        "Thanks bye",
        "thank you",
        "gibberish askdfjhas",
        "what is the meaning of life"
    ]
    
    for test_input in test_inputs:
        print(f"User: {test_input}")
        print(f"Idosia: {get_chatbot_response(test_input)}")
        print("---")

    # Interactive test
    # Interactive test removed as it causes EOFError in non-interactive environments
    # print("\nInteractive Test (type 'quit' to exit):")
    # while True:
    #     user_query = input("You: ")
    #     if user_query.lower() == 'quit':
    #         break
    #     print(f"Idosia: {get_chatbot_response(user_query)}")
