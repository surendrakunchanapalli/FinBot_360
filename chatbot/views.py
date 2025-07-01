from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os, logging
from datetime import datetime
from langchain_core.callbacks import StdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.chat_message_histories import FileChatMessageHistory

from .tools import get_current_date, calculate_age_from_year, bank_rag_search, find_branch_by_city, generate_account_opening_steps
from .llm_config import llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0.5,
#     google_api_key=os.environ["GOOGLE_API_KEY"]
# )

memory = ConversationBufferMemory(
    memory_key="chat_history",  # MUST be this key name
    chat_memory=FileChatMessageHistory("chat_memory.json"),
    return_messages=True        # VERY important to avoid str error
)


tools = [
    Tool(
        name = "GetCurrentDate",
        func = lambda _: get_current_date(), 
        description = "Use this to answer questions like 'What is the date or time today?'."
    ),
    Tool(
        name = "CalculateAgeFromYear",
        func = calculate_age_from_year,
        description = "Use to calculate age when user says something like 'I was born in 2000 or 2000-09-10' or Sep 10 1999 or March 17 1999."
    ),
    Tool(
        name="BankDocumentSearch",
        func=bank_rag_search,
        description="Use this tool to search banking-related information like KYC, account opening, documents, etc."
    ),
    Tool(
        name="FindBranchByCity",
        func=find_branch_by_city,
        description="Use to check if we have a bank branch in a specific city like Hyderabad or Delhi."
    ),
    Tool(
        name="GenerateAccountOpeningSteps",
        func=generate_account_opening_steps,
        description="Use to provide step-by-step instructions for opening a bank account."
    ),
    Tool(
        name="GeneralChat",
        func=lambda q: llm.invoke(q).content,
        description="Use this when the user's question is not related to banking and needs general knowledge"
    )


]

callback = StdOutCallbackHandler()

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    callbacks=[callback],
    agent_kwargs={
        "system_message": (
            "Your name FinBot 360, You were created and introduced by Surendra. If someone asks who created or introduced you, mention their my name. you can give Bank Related information and general knowledge question's Answer's also"
            "You are a helpful assistant, primarily focused on banking, but you can also answer general questions."
            "You also answer general questions like weather, history, technology, or personal queries. "
            "If the user asks something unrelated to banking, you can still try to help using your general knowledge."
            "You are a helpful assistant. If the user asks about today's date or their age, "
            "If user says 'I was born in 2000-09-10', extract the year (2000) and calculate age."
            "You are FinBot 360, a virtual assistant for XYZ Bank. You help users with banking information, complaints, account help, and branch info. "
            "You also answer common questions like: 'How to apply for a loan?', 'What documents are required for KYC?', or 'Where is the nearest branch?'. "
            "If the answer is not found in your memory or tools, ask for more details or apologize."
        )
        
    }
)

def index(request):
    return render(request, "index.html")

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message")

            if not user_input:
                return JsonResponse({"error": "No message provided"}, status=400)
            
            # response = llm.invoke(user_input)
            # return JsonResponse({"response": response.content})

            response = agent.invoke({"input": user_input})
            return JsonResponse({"response": response['output']})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

# Create your views here.
