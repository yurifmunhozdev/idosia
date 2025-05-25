import nltk
import os
import openai

# --- OpenAI API Setup ---
openai.api_key = os.environ.get("OPENAI_API_KEY")
llm_enabled = bool(openai.api_key)

if not llm_enabled:
    print("Warning: OPENAI_API_KEY not set. LLM features will be disabled. The chatbot will rely on rule-based responses.")

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
    "greeting": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "ola", "oi"], # Added "ola", "oi"
    "farewell": ["bye", "thanks", "thank", "thankyou", "farewell", "see you", "appreciate it", "tchau", "obrigado", "obrigada"], # Added "tchau", "obrigado/a"
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

# --- LLM API Function ---
def get_llm_api_response(user_query: str) -> str:
    if not llm_enabled:
        return "Desculpe, minha funcionalidade avançada de IA está temporariamente indisponível."

    system_prompt = """
    Você é o Idosia Assistant, um assistente virtual de saúde focado em fornecer informações gerais sobre saúde e bem-estar para idosos.
    Seu propósito é oferecer informações educativas e de suporte sobre parâmetros de saúde comuns, dicas de bem-estar geral e como usar o aplicativo Idosia.
    Restrições importantes:
    1. NÃO forneça aconselhamento médico direto.
    2. NÃO diagnostique condições.
    3. NÃO sugira tratamentos específicos para doenças.
    4. SEMPRE direcione o usuário a consultar um profissional de saúde (médico, enfermeiro, etc.) para questões de saúde pessoal, diagnósticos ou planos de tratamento.
    5. Seja empático, claro e use uma linguagem acessível.
    6. Responda em Português do Brasil.
    7. Se você não souber a resposta para uma pergunta específica ou se ela estiver fora do seu escopo (por exemplo, pedir para interpretar dados médicos complexos ou dar conselhos financeiros), admita educadamente que não pode ajudar com essa questão específica e reforce a necessidade de consultar um especialista apropriado.
    8. Mantenha as respostas concisas e informativas.
    9. Você pode falar sobre o que é pressão alta em geral, mas não pode dizer se a pressão do usuário está alta ou o que ele deve fazer para baixar a pressão dele especificamente.
    10. Você pode explicar o que é colesterol LDL, mas não pode interpretar os resultados de exames de colesterol do usuário.
    """
    try:
        print(f"DEBUG: Sending to LLM (get_llm_api_response): {user_query}")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=300 
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Desculpe, estou com dificuldades para acessar minha base de conhecimento externa no momento. Por favor, tente novamente mais tarde ou pergunte sobre algo que eu possa responder diretamente."

# --- Main Chatbot Logic Function ---
def get_chatbot_response(user_input: str) -> str:
    user_input_lower = user_input.lower()
    tokens = nltk.word_tokenize(user_input_lower)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # 1. Handle simple, predefined intents first
    if any(keyword in user_input_lower for keyword in keywords.get("greeting", [])):
        return responses.get("greeting", "Olá! Como posso ajudar?")
    
    if any(keyword in user_input_lower for keyword in keywords.get("farewell", [])):
        if not any(neg_kw in user_input_lower for neg_kw in ["not thank", "no thanks"]): # Avoid "no thanks" triggering farewell
            return responses.get("farewell", "Até logo!")

    # 2. If no simple rule matches AND llm_enabled is true, try LLM
    #    (but perhaps avoid LLM for very specific app questions that rules handle well)
    #    For now, let's assume if it's not a greeting/farewell, it *could* go to LLM.
    #    More nuanced routing can be added later.
    if llm_enabled:
        # Potentially, add checks here for queries that are *better* handled by rules
        # even if LLM is on (e.g., "how to input data" might be too specific for LLM general knowledge)
        # For now, let's test the general LLM path for non-greeting/farewell:
        print(f"DEBUG: Potentially sending to LLM (get_chatbot_response): {user_input}")
        # A more robust check might be needed here to decide if it's truly an LLM candidate
        # For this iteration, any non-greeting/farewell will try LLM if enabled.
        return get_llm_api_response(user_input)

    # 3. Fallback to comprehensive rule-based logic if LLM is disabled or not used for the query
    print(f"DEBUG: LLM disabled or query not sent to LLM. Using rule-based fallback for: {user_input}")
    
    # Specific Health Tips first
    if any(phrase in user_input_lower for phrase in keywords["lower_bp_tips"]):
        return responses["health_tip_bp"]

    # App Usage Guidance - These specific phrases should be checked BEFORE greetings (already handled, but kept for structure)
    if "how to use this app" in user_input_lower or \
       any(phrase in user_input_lower for phrase in keywords["app_usage"] if phrase == "how to use this app"):
         return responses["app_input_guidance"] 
    if "view history" in user_input_lower or \
       any(phrase in user_input_lower for phrase in keywords["app_dashboard"] if phrase == "view history"):
        return responses["app_dashboard_guidance"]

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
    if any(keyword in lemmatized_tokens for keyword in keywords["app_input"]): # Redundant check if covered by phrases
        return responses["app_input_guidance"]
    if any(keyword in lemmatized_tokens for keyword in keywords["app_dashboard"]): # Redundant check
        return responses["app_dashboard_guidance"]
        
    # General Health Tips
    if any(keyword in user_input_lower for keyword in keywords["health_tips"]) or \
       any(token in lemmatized_tokens for token in ["tip", "advice", "suggest", "recommend"]):
        return responses["health_tip_general"]

    # 4. Default response if no rule matches anywhere
    return responses.get("default", "Desculpe, não entendi bem. Pode reformular?")


if __name__ == '__main__':
    # Test with LLM (requires OPENAI_API_KEY to be set in environment)
    print("Idosia Chatbot Test Mode (with potential LLM integration):")
    print("----------------------------------------------------------")
    
    # If OPENAI_API_KEY is not set, these will all use rule-based or default.
    # If it IS set, non-greeting/farewell will try the LLM.
    test_queries = [
        "Olá", # Rule-based
        "Oi, tudo bem?", # Rule-based
        "O que é hipertensão?", # LLM if enabled
        "Explique colesterol LDL.", # LLM if enabled
        "Como posso usar o aplicativo Idosia para registrar meus dados?", # Rule-based (fallback if LLM disabled, or direct if LLM path refined)
        "Me dê uma dica de saúde geral.", # Rule-based (fallback if LLM disabled) or LLM
        "Obrigado, até mais!", # Rule-based
        "Qual a capital da França?" # Should be handled by LLM or default rule-based
    ]

    for query in test_queries:
        print(f"User: {query}")
        response = get_chatbot_response(query)
        print(f"Idosia: {response}")
        print("-" * 20)

    # You can add more specific tests for rule-based logic when LLM is disabled
    if not llm_enabled:
        print("\nTesting specific rule-based responses (since LLM is disabled):")
        rule_based_tests = [
            "Como vejo meu histórico?", # app_dashboard_guidance
            "O que é creatinina?", # creatinine_info
            "Dicas para pressão arterial", # health_tip_bp
        ]
        for query in rule_based_tests:
            print(f"User: {query}")
            response = get_chatbot_response(query) # LLM path won't be taken
            print(f"Idosia: {response}")
            print("-" * 20)
