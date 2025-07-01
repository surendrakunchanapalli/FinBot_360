# tools.py
from datetime import datetime
import logging
from .rag_tools import get_rag_chain
from .llm_config import llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_current_date():
    today = datetime.now()
    response = today.strftime("Today's date is %Y-%m-%d and the time is %H:%M:%S.")
    logger.info(f"[Tool Userd] get_current_date() -> {response}")
    return response

def calculate_age_from_year(input_str : str):
    try:
        input_str = input_str.strip()
        formats = ["%Y", "%Y-%m-%d", "%b %d %Y", "%B %d %Y"]
        birth_year = None
        
        for fmt in formats:
            try:
                dt = datetime.strptime(input_str, fmt)
                birth_year = dt.year
                break
            except ValueError:
                continue
            
        age = datetime.today().year - birth_year
        result = f"If you were born in {birth_year}, your age is {age}."
        logger.info(f"[Tool Used] calculate_age_from_year({input_str}) -> {result}")
        return result
    
    except Exception as e:
        logger.error(f"[Tool Error] Invalid Input: {input_str} | {e}")
        return "Please provide a valid birth year or date like '2000', '2000-09-10', or 'Sep 10 2000'"
    
USE_RAG = True  # Set to True when real RAG is ready

def bank_rag_search(query: str) -> str:
    if USE_RAG:
        try:
            rag_chain = get_rag_chain()
            result = rag_chain.run(query)
            logger.info(f"[Tool Used] RAG -> {query} => {result}")
            return result
        except Exception as e:
            logger.error(f"[RAG Failed] {e} | Falling back to general LLM")
            return llm.invoke(query).content
    else:
        # basic mock answers (you can remove this if using real docs)
        if "kyc" in query.lower():
            return "KYC documents required: Aadhaar, PAN card, and a passport-sized photo."
        elif "account open" in query.lower():
            return "Visit a nearby branch or website, fill out a form, submit KYC, and deposit initial balance."
        else:
            logger.warning("[Tool] Falling back to LLM for general query")
            return llm.invoke(query).content


def find_branch_by_city(city: str) -> str:
    # Simulated city-wise branch info (replace with real data later)
    city = city.lower()
    branches = {
        "hyderabad": "Yes, we have 5 branches in Hyderabad.",
        "mumbai": "Yes, our headquarters is in Mumbai with 8 branches.",
        "delhi": "Yes, 3 branches in Delhi, including Connaught Place."
    }
    result = branches.get(city, f"Sorry, no branch information found for {city.title()}.")
    logger.info(f"[Tool Used] find_branch_by_city({city}) -> {result}")
    return result

def generate_account_opening_steps(_: str = "") -> str:
    steps = (
        "1. Visit the bank branch or website\n"
        "2. Fill the account opening form\n"
        "3. Submit KYC documents (Aadhaar, PAN, etc.)\n"
        "4. Deposit the minimum balance\n"
        "5. Collect your account kit or get it digitally"
    )
    logger.info(f"[Tool Used] generate_account_opening_steps() -> {steps}")
    return steps