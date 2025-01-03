import os
from semantic_router import Route, RouteLayer
from semantic_router.encoders import CohereEncoder
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def setup_routes():
   
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    # Initialize the CohereEncoder
    encoder = CohereEncoder()

    # Define routes 
    application_route = Route(
        name="APPLICATION_ROUTE",
        utterances=[
            "How do I apply for scholarship",
            "I need scholarship. What do I do",
            "Scholarship application process",
            "I want to apply for Scholarship application ",
            "I want to apply for Scholarship",
            "How can I apply for the scholarship?",
            "How can I apply for a scholarship?", 
            "What is the scholarship application process?",
            "What are the steps involved in applying for a scholarship?",
            "How do I go about applying for scholarships?",
            "I need a scholarship. What do I do?",
            "I need financial assistance for education. How can I apply for scholarships?",
            "What are the immediate steps I can take to apply for a scholarship?",
            "Could you please explain the scholarship application procedure?",
            "What are the formal requirements for applying for a scholarship?",
            "I am interested in applying for scholarships. What is the first step?",
            "How are scholarships applied for?",
            "By what process can scholarships be obtained?",
            "May I inquire about the scholarship application process?",
            "Could you please provide me with information on how to apply for scholarships?",
            "How can I determine if I am eligible for any scholarships?",
            "What are the eligibility criteria for applying for scholarships?",
            "Where can I find information on available scholarships?",
            "How do I locate scholarships that I may be eligible for?", 
            "Can you guide me through the application process for a scholarship?", 
            "What steps are needed to apply for scholarships?", 
            "How do I start a scholarship application?", 
            "What is the procedure for applying for a scholarship?", 
            "What’s the process for submitting a scholarship application?", 
            "Where can I find instructions to apply for scholarships?", 
            "How do I begin the scholarship application process?", 
            "What are the requirements for applying for a scholarship?", 
            "What do I need to do to apply for a scholarship?", 
            "How do I initiate the process for scholarship application?", 
            "Can you explain how to apply for scholarships?", 
            "What’s the process for getting a scholarship?", 
            "How do I go about applying for scholarships?", 
            "What’s the correct way to apply for scholarships?", 
            "Where can I find information on scholarship applications?", 
            "What’s the best way to apply for scholarships?", 
            "How should I proceed to apply for a scholarship?", 
            "How do I make a scholarship application?", 
            "Can you help me apply for scholarships?", 
            "What’s the first step in a scholarship application?", 
            "Can I get guidance on how to apply for scholarships?", 
            "What should I do to submit a scholarship application?", 
            "Can you walk me through the steps to apply for scholarships?", 
            "How do I complete the scholarship application process?", 
            "How can I register for a scholarship application?", 
            "How does the scholarship application process work?", 
            "Can I apply for scholarships online?", 
            "What’s involved in applying for a scholarship?", 
            "Where do I submit my scholarship application?", 
            "How long does it take to apply for scholarships?", 
            "What platform is used to apply for scholarships?", 
            "Do I need to submit any forms to apply for a scholarship?", 
            "Is there an online portal for scholarship applications?", 
            "What’s the eligibility to apply for scholarships?", 
            "Are there specific dates for applying for scholarships?", 
            "Can you provide a link to the scholarship application form?", 
            "What are the deadlines for applying for scholarships?", 
            "How do I confirm my scholarship application was received?", 
            "Can I edit my scholarship application after submission?", 
            "Is there an application fee for scholarships?", 
            "Where can I find updates on my scholarship application process?", 
            "Can you help me fill out my scholarship application form?", 
            "Are there templates for scholarship applications?", 
            "What should I avoid while applying for scholarships?", 
            "Can I apply for multiple scholarships at once?", 
            "Do I need a recommendation letter to apply for scholarships?", 
            "What documents do I need to apply for scholarships?", 
            "Where can I track my scholarship application progress?", 
            "How do I resubmit my scholarship application if needed?"
        ],
        score_threshold=0.7
    )
    
    documents_route = Route(
        name="DOCUMENTS_ROUTE",
        utterances=[
            "What documents are required for applying for scholarship",
            "How do I submit documents for scholarship",
            "What documents are required to apply for scholarships?",
            "What documents are required for scholarship applications?",
            "What documents do I need to submit for a scholarship?",
            "What are the required documents for scholarship applications?",
            "How do I submit the necessary documents for a scholarship?",
            "What type of documents are typically required for scholarship applications?",
            "Are there specific documents required for this particular scholarship?",
            "What supporting documentation is needed for my scholarship application?",
            "How do I submit the required documents for a scholarship?",
            "Where should I submit the scholarship documents?",
            "What is the process for submitting scholarship documents?",
            "Can I submit documents electronically?",
            "Could you please provide a list of required documents for scholarship applications?",
            "What is the acceptable method for submitting scholarship documents?",
            "How are scholarship documents submitted?",
            "By what means can scholarship documents be submitted?",
            "May I inquire about the required documents for scholarship applications?",
            "Could you please inform me of the document submission process?", 
            "Can you provide a list of necessary documents for scholarships?", 
            "What paperwork is needed for scholarship applications?", 
            "What supporting documents do I need for scholarships?", 
            "Are there specific forms needed to apply for scholarships?", 
            "What are the document requirements for scholarships?", 
            "How do I know what documents to submit for scholarships?", 
            "Can I get a checklist of required scholarship documents?", 
            "What is the documentation process for scholarships?", 
            "Are transcripts required for scholarship applications?", 
            "Do I need to submit any ID for scholarship applications?", 
            "Are academic records necessary for scholarships?", 
            "How do I prepare my documents for scholarship applications?", 
            "Do I need a letter of recommendation for scholarships?",  
            "What financial documents are needed for scholarships?", 
            "Can I submit scanned copies of documents for scholarships?", 
            "What happens if I miss a required document for scholarships?", 
            "Where can I upload my scholarship documents?", 
            "Is there a template for scholarship documents?",  
            "Are digital documents accepted for scholarships?", 
            "What formats are allowed for scholarship documents?", 
            "What should I include in my scholarship application file?", 
            "How do I verify my scholarship documents are complete?", 
            "Do I need proof of citizenship for scholarships?", 
            "What’s the deadline for submitting scholarship documents?", 
            "How do I update documents for my scholarship application?", 
            "Can I mail my scholarship documents physically?", 
            "Where can I get help preparing scholarship documents?", 
            "What’s the procedure to upload additional documents?", 
            "Do I need both hard and soft copies of documents?", 
            "Is an income certificate needed for scholarships?", 
            "What happens if I upload incorrect documents?", 
            "Can I preview my document submission for scholarships?", 
            "Are there size limits for scholarship document uploads?", 
            "Do I need an affidavit for scholarships?", 
            "What’s the process for resubmitting missing documents?", 
            "Do scholarships require scanned or photographed documents?"

        ],
        score_threshold=0.7
    )
    
    status_route = Route(
        name="STATUS_ROUTE",
        utterances=[
            "What is the status of my application",
            "Current status",
            "Application status",
            "Scholarship status",
            "What is the status of my application?",
            "What is the current status of my application?",
            "What is the application status?",
            "What is the scholarship status?",
            "Could you please provide me with an update on the status of my application?",
            "I would like to inquire about the current status of my scholarship application.",
            "What is the status of the application I submitted?",
            "What is the current status of my application being reviewed?",
            "May I inquire about the current status of my scholarship application?",
            "Could you please let me know the status of my application?",
            "Has my application been reviewed?",
            "What’s the status of my scholarship application?", 
            "How can I check the progress of my application?", 
            "What is the update on my scholarship request?", 
            "Can you tell me the current state of my application?", 
            "Has my scholarship application been processed?", 
            "Where is my scholarship application currently?", 
            "What’s the latest update on my scholarship status?", 
            "What’s the condition of my application right now?", 
            "Can you provide the current status of my application?", 
            "How do I verify the status of my application?", 
            "Has my application been reviewed yet?", 
            "What stage is my scholarship application in?", 
            "Is my scholarship application still under review?", 
            "Can you update me on my scholarship application progress?", 
            "How do I track the status of my application?", 
            "What’s the decision on my scholarship application?", 
            "Has my scholarship application been approved yet?", 
            "Can you confirm if my application was received?", 
            "What does the portal say about my scholarship status?", 
            "How long does it take to get a status update?", 
            "Can I expect any news about my scholarship soon?", 
            "Is there any pending action for my application?", 
            "Has my application been forwarded to the committee?", 
            "What’s the decision timeline for my scholarship application?", 
            "Where can I see detailed updates about my application?", 
            "What’s the final status of my scholarship request?", 
            "Have there been any updates to my application?", 
            "When will I receive the final verdict on my scholarship?", 
            "Is my application currently active or closed?", 
            "Are there any issues with my scholarship application?", 
            "Has my scholarship been awarded yet?", 
            "What’s holding up my scholarship approval?", 
            "Can you escalate my application review?", 
            "What’s the pending status for my scholarship?", 
            "What happens next for my scholarship application?", 
            "Can you give me a status breakdown for my application?", 
            "How do I resolve delays in my scholarship review?", 
            "What does the current update mean for my scholarship?", 
            "Has my scholarship funding been approved?", 
            "When can I expect the scholarship disbursement?", 
            "Has my application been marked as complete?", 
            "Is my scholarship award in progress?", 
            "What happens after my scholarship is approved?"    
        ],
        score_threshold=0.7
    )
    
    other_relevant_route = Route(
        name="OTHER_RELEVANT",
        utterances=[
            "Any other application-related questions"
        ],
        score_threshold=0.7
    )
    
    # Add all routes to a list
    routes = [application_route, documents_route, status_route, other_relevant_route]
    
    # Set up RouteLayer with encoder
    rl = RouteLayer(encoder=encoder, routes=routes)
    return rl

# Setup routes at the global level
rl = setup_routes()

def handle_user_query(user_prompt):
    
    # Function to handle user queries and determine the route.
    route = rl(user_prompt)
    
    if route:
        return {
            'response': f"Handling query related to {route.name}.",
            'route_name': route.name,
            'status': 'SUCCESS'
        }
    else:
        return {
            'response': 'The question does not match our criteria. Please ask another question or contact support for more help.',
            'status': 'FAILED'
        }


if __name__ == "__main__":
    while(True):
        user_question = input("Enter your question: ")
        result = handle_user_query(user_question)
        print(result)
