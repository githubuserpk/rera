from flask import Flask, jsonify, request
import chromadb
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import vertexai
import os
import functools
from chromadb.config import Settings

app = Flask(__name__)

# Initialize Vertex AI
PROJECT_ID = "pk-aiproject"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Initialize models
embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
gemini_model = GenerativeModel("gemini-2.0-flash-lite-001")


background_information = """
    You are a helpful expert in legal matters on Artificial Intelligence specifically the EU AI Act.
    You know that the EU AI Act is a comprehensive legal Regulation for Artificial Intelligence which takes a risk based 
    assessment of the AI Systems.  
    You need to look into the Articles and the related Annexures before answering the user queries. 
    Please note that the Act is organized into the following hierarchy

    There are totally 13 Chapters, Chapter I to Chapter XIII and a total of 113 Articles

    Chapter I: General Provisions
    Article 1: Subject Matter
    Article 2: Scope
    Article 3: Definitions
    Article 4: AI literacy

    Chapter II: Prohibited AI Practices
    Article 5: Prohibited AI Practices

    Chapter III:
    High-Risk AI System
    Section 1: Classification of AI Systems as High-Risk
    Article 6: Classification Rules for High-Risk AI Systems
    Article 7: Amendments to Annex III
    Section 2: Requirements for High-Risk AI Systems
    Article 8: Compliance with the Requirements
    Article 9: Risk Management System
    Article 10: Data and Data Governance
    Article 11: Technical Documentation
    Article 12: Record-Keeping
    Article 13: Transparency and Provision of Information to Deployers
    Article 14: Human Oversight
    Article 15: Accuracy, Robustness and Cybersecurity
    Section 3: Obligations of Providers and Deployers of High-Risk AI Systems and Other Parties
    Article 16: Obligations of Providers of High-Risk AI Systems
    Article 17: Quality Management System
    Article 18: Documentation Keeping
    Article 19: Automatically Generated Logs
    Article 20: Corrective Actions and Duty of Information
    Article 21: Cooperation with Competent Authorities
    Article 22: Authorised Representatives of Providers of High-Risk AI Systems
    Article 23: Obligations of Importers
    Article 24: Obligations of Distributors
    Article 25: Responsibilities Along the AI Value Chain
    Article 26: Obligations of Deployers of High-Risk AI Systems
    Article 27: Fundamental Rights Impact Assessment for High-Risk AI Systems
    Section 4: Notifying Authorities and Notified Bodies
    Article 28: Notifying Authorities
    Article 29: Application of a Conformity Assessment Body for Notification
    Article 30: Notification Procedure
    Article 31: Requirements Relating to Notified Bodies
    Article 32: Presumption of Conformity with Requirements Relating to Notified Bodies
    Article 33: Subsidiaries of Notified Bodies and Subcontracting
    Article 34: Operational Obligations of Notified Bodies
    Article 35: Identification Numbers and Lists of Notified Bodies
    Article 36: Changes to Notifications
    Article 37: Challenge to the Competence of Notified Bodies
    Article 38: Coordination of Notified Bodies
    Article 39: Conformity Assessment Bodies of Third Countries
    Section 5: Standards, Conformity Assessment, Certificates, Registration
    Article 40: Harmonised Standards and Standardisation Deliverables
    Article 41: Common Specifications
    Article 42: Presumption of Conformity with Certain Requirements
    Article 43: Conformity Assessment
    Article 44: Certificates
    Article 45: Information Obligations of Notified Bodies
    Article 46: Derogation from Conformity Assessment Procedure
    Article 47: EU Declaration of Conformity
    Article 48: CE Marking
    Article 49: Registration

    Chapter IV: Transparency Obligations for Providers and Deployers of Certain AI Systems
    Article 50: Transparency Obligations for Providers and Deployers of Certain AI Systems

    Chapter V: General-Purpose AI Models
    Section 1: Classification Rules
    Article 51: Classification of General-Purpose AI Models as General-Purpose AI Models with Systemic Risk
    Article 52: Procedure
    Section 2: Obligations for Providers of General-Purpose AI Models
    Article 53: Obligations for Providers of General-Purpose AI Models
    Article 54: Authorised Representatives of Providers of General-Purpose AI Models
    Section 3: Obligations of Providers of General-Purpose AI Models with Systemic Risk
    Article 55: Obligations for Providers of General-Purpose AI Models with Systemic Risk
    Section 4: Codes of Practice
    Article 56: Codes of Practice

    Chapter VI:
    Measures in Support of Innovation
    Article 57: AI Regulatory Sandboxes
    Article 58: Detailed Arrangements for, and Functioning of, AI Regulatory Sandboxes
    Article 59: Further Processing of Personal Data for Developing Certain AI Systems in the Public Interest in the AI Regulatory Sandbox
    Article 60: Testing of High-Risk AI Systems in Real World Conditions Outside AI Regulatory Sandboxes
    Article 61: Informed Consent to Participate in Testing in Real World Conditions Outside AI Regulatory Sandboxes
    Article 62: Measures for Providers and Deployers, in Particular SMEs, Including Start-Ups
    Article 63: Derogations for Specific Operators

    Chapter VII:
    Governance
    Section 1: Governance at Union Level
    Article 64: AI Office
    Article 65: Establishment and Structure of the European Artificial Intelligence Board
    Article 66: Tasks of the Board
    Article 67: Advisory Forum
    Article 68: Scientific Panel of Independent Experts
    Article 69: Access to the Pool of Experts by the Member States
    Section 2: National Competent Authorities
    Article 70: Designation of National Competent Authorities and Single Point of Contact
    
    Chapter VIII: EU Database for High-Risk AI Systems
    Article 71: EU Database for High-Risk AI Systems Listed in Annex III

    Chapter IX: Post-Market Monitoring, Information Sharing and Market Surveillance
    Section 1: Post-Market Monitoring
    Article 72: Post-Market Monitoring by Providers and Post-Market Monitoring Plan for High-Risk AI Systems
    Section 2: Sharing of Information on Serious Incidents
    Article 73: Reporting of Serious Incidents
    Section 3: Enforcement
    Article 74: Market Surveillance and Control of AI Systems in the Union Market
    Article 75: Mutual Assistance, Market Surveillance and Control of General-Purpose AI Systems
    Article 76: Supervision of Testing in Real World Conditions by Market Surveillance Authorities
    Article 77: Powers of Authorities Protecting Fundamental Rights
    Article 78: Confidentiality
    Article 79: Procedure at National Level for Dealing with AI Systems Presenting a Risk
    Article 80: Procedure for Dealing with AI Systems Classified by the Provider as Non-High-Risk in Application of Annex III
    Article 81: Union Safeguard Procedure
    Article 82: Compliant AI Systems Which Present a Risk
    Article 83: Formal Non-Compliance
    Article 84: Union AI Testing Support Structures
    Section 4: Remedies
    Article 85: Right to Lodge a Complaint with a Market Surveillance Authority
    Article 86: Right to Explanation of Individual Decision-Making
    Article 87: Reporting of Infringements and Protection of Reporting Persons
    Section 5: Supervision, Investigation, Enforcement and Monitoring in Respect of Providers of General-Purpose AI Models
    Article 88: Enforcement of the Obligations of Providers of General-Purpose AI Models
    Article 89 : Monitoring Actions
    Article 90: Alerts of Systemic Risks by the Scientific Panel
    Article 91: Power to Request Documentation and Information
    Article 92: Power to Conduct Evaluations
    Article 93: Power to Request Measures
    Article 94: Procedural Rights of Economic Operators of the General-Purpose AI Model

    Chapter X: Codes of Conduct and Guidelines
    Article 95: Codes of Conduct for Voluntary Application of Specific Requirements
    Article 96: Guidelines from the Commission on the Implementation of this Regulation

    Chapter XI:
    Delegation of Power and Committee Procedure
    Article 97: Exercise of the Delegation
    Article 98: Committee Procedure

    Chapter XII: Penalties
    Article 99: Penalties
    Article 100: Administrative Fines on Union Institutions, Bodies, Offices and Agencies
    Article 101: Fines for Providers of General-Purpose AI Models


    Chapter XIII:
    Final Provisions
    Article 102: Amendment to Regulation (EC) No 300/2008
    Article 103: Amendment to Regulation (EU) No 167/2013
    Article 104: Amendment to Regulation (EU) No 168/2013
    Article 105: Amendment to Directive 2014/90/EU
    Article 106: Amendment to Directive (EU) 2016/797
    Article 107: Amendment to Regulation (EU) 2018/858
    Article 108: Amendments to Regulation (EU) 2018/1139
    Article 109: Amendment to Regulation (EU) 2019/2144
    Article 110: Amendment to Directive (EU) 2020/1828
    Article 111: AI Systems Already Placed on the Market or put into Service and General-Purpose AI Models Already Placed on the Marked
    Article 112: Evaluation and Review
    Article 113: Entry into Force and Application    


    Your users are asking questions about information contained in the EU AI Act.
    You need to scan through all the content that contains the Chapters and Annexes and the Recitals.

    The Annexes are organized as follows: 
    Annex 1 to Annex 13 
    Annex I: List of Union Harmonisation Legislation
    Annex II: List of Criminal Offences Referred to in Article 5(1), First Subparagraph, Point (h)(iii)
    Annex III: High-Risk AI Systems Referred to in Article 6(2)
    Annex IV: Technical Documentation Referred to in Article 11(1)
    Annex V: EU Declaration of Conformity
    Annex VI: Conformity Assessment Procedure Based on Internal Control
    Annex VII: Conformity Based on Assessment of the Quality Management System and an Assessment of the Technical Documentation 
    Annex VIII: Information to be Submitted upon the Registration of High-Risk AI Systems in Accordance with Article 49
    Annex IX: Information to be Submitted upon the Registration of High-Risk AI Systems Listed in Annex III in Relation to Testing in Real World Conditions in Accordance with Article 60
    Annex X: Union Legislative Acts on Large-Scale IT Systems in the Area of Freedom, Security and Justice
    Annex XI: Technical Documentation Referred to in Article 53(1), Point (a) – Technical Documentation for Providers of General-Purpose AI Models
    Annex XII: Transparency Information Referred to in Article 53(1), Point (b) – Technical Documentation for Providers of General-Purpose AI Models to Downstream Providers that Integrate the Model into Their AI System
    Annex XIII: Criteria for the Designation of General-Purpose AI models with Systemic Risk Referred to in Article 51

    The Recitals are organized as follows: 
    Recital 1 to Recital 180

    The Recitals may refer back one or more Articles and Annexes

    """


# Create Chroma client
client = chromadb.PersistentClient(path="../datalake/embeddings/chromadb",         
            settings=Settings(
            anonymized_telemetry=False,  # Disable telemetry
            is_persistent=True,
            allow_reset=False,  # Prevent accidental resets
        ))

@functools.lru_cache(maxsize=None)
def merge_files(folder_path):
    merged_content = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
                merged_content.append(file_content)
    return "\n\n".join(merged_content)

@functools.lru_cache(maxsize=None)
def initialize_collection():
    loader = PyPDFLoader("../datalake/data_sources/eu-ai-act-full_regulation_text_ENG.pdf")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    articles_chunks = text_splitter.split_documents(documents)
    for chunk in articles_chunks:
        chunk.metadata["source"] = "pdfarticle" #assign metadata to the pdf


    annexes_text = merge_files("../datalake/data_sources/annexes")
    annexes_chunks = text_splitter.create_documents([annexes_text], metadatas=[{"source": "annexes"}])
    

    recitals_text = merge_files("../datalake/data_sources/recitals")
    recitals_chunks = text_splitter.create_documents([recitals_text], metadatas=[{"source": "recitals"}])

    all_chunks = articles_chunks + annexes_chunks + recitals_chunks

    collection = client.get_or_create_collection("eu_ai_act")

    for i, chunk in enumerate(all_chunks):
        embedding = embedding_model.get_embeddings([chunk.page_content])[0]

        collection.add(
            documents=[chunk.page_content],
            embeddings=[embedding.values],
            ids=[f"chunk_{i}"],
            metadatas=[{"source": chunk.metadata.get("source", "pdfarticle")}] #set default value to pdfarticle if nothing is found
        )

    return collection

def get_collection():
    if 'COLLECTION' not in app.config:
        app.config['COLLECTION'] = initialize_collection()
    return app.config['COLLECTION']

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    collection = get_collection()
    query_embedding = embedding_model.get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding.values],
        n_results=10
    )
    context = results['documents'][0]
    response = generate_response(query, context)
    return jsonify({"response": response})


@app.route('/recommendation', methods=['POST'])
def recommendation():
    query = request.json['query']
    collection = get_collection()
    query_embedding = embedding_model.get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding.values],
        n_results=10
    )
    context = results['documents'][0]
    response = generate_recommendation(query, context)
    return jsonify({"response": response})



def generate_recommendation(query, context):

    prompt = f"""
    The background is: {background_information}

    Question: {query}
    Given the above background and the users question you need to do the following: 

    Before answering go through the act as per the guidelines provided in the background information
    and provide your response accordingly.      

    You should summarize the content that can be easily understood by a human.
        
    Provide the top 10 actions they need to take to be compliant with the EU AI Act
    Your recommendation should be relavant to the scenario given by the user.

    You should point out under which risk category they fall into ie whether prohibited risk or high risk or 
    limited risk or no risk.
    You should also list the penalties in case of breach of the EU AI Act.  
    You should also mention what are the Transparency obligations    
    You should also mention the deadline and when the compliance is due to help user prepare for compliance.
    Please refer to the background information to come up with your answers. 

    Context: {context}
    
    Answer:"""
    
    response = gemini_model.generate_content(prompt)
    return response.text




def generate_response(query, context):
    prompt = f"""
    The background is: {background_information}

    Answer the following question using only the information provided in the context below.
    When you answer please provide citations and mention the Chapter Section Article Annex and the Recital so that 
    the user can look into them for further analysis.

    If the output has links to Annexes or Recitals provide a hyperlink so that user can click on it for further analysis.
    
    Question: {query}
    
    Context: {context}
    
    Answer:"""
    
    response = gemini_model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    app.run(port=5000)
