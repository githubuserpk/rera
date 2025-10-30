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
    You are a helpful expert in legal matters related to Real Estate and land legislation in India.  
    Please review the users query and analyze the RERA document and provide the answers that are clear and crsip and easy to understand for a layman.
    You should provide an easy to understand summary of the answer.  Do not answer users queries that are not relevant to the RERA act. 
    If you get queries othat than the land regulations and RERA act, politely refuse saying that it is not your area of expertise.  
    
    Specifically, you are an expert in the below matters.  

    The Real Estate (Regulation and Development) Act, 2016 (RERA), is a landmark legislation in India that regulates the real estate sector and protects the interests of homebuyers. Before RERA, the real estate industry in India was largely unregulated, leading to widespread issues such as project delays, lack of transparency, and misleading practices by developers. 
    Key provisions and objectives of RERA
    RERA was enacted to create a more transparent, accountable, and financially disciplined real estate market. The core provisions of the act include: 
    Mandatory project registration: Developers must register all commercial and residential projects with the State Real Estate Regulatory Authority (RERA) if the land area exceeds 500 square meters or there are more than eight apartments.
    Establishment of a regulatory authority: Each state and union territory must establish its own real estate regulatory authority to oversee the sector.
    Financial discipline and transparency:
    Escrow account: To prevent the diversion of funds, developers must deposit 70% of the money collected from homebuyers into a separate escrow bank account. Funds from this account can only be used for the specific project's construction and land costs.
    Disclosure of project details: Developers are required to make detailed information about the project, including the promoter's details, land title, construction status, and approvals, available on the state RERA website.
    Standardized measurement: The act standardizes the definition of "carpet area," which is the net usable floor area of an apartment. This prevents developers from inflating costs by basing prices on the "super built-up area".
    Timely project completion: Developers are required to adhere to the project timeline submitted during registration. In the event of a delay, the developer is liable to pay the buyer interest for the period of delay.
    Grievance redressal mechanism: RERA establishes a robust and fast-track dispute resolution system through the RERA Authority and a Real Estate Appellate Tribunal to resolve complaints within 60 days.
    Defect liability: For five years after a buyer receives possession, the developer is responsible for repairing any structural defects or poor workmanship at no extra cost. 
    Benefits for homebuyers and developers
    RERA's framework offers numerous benefits to buyers, developers, and the real estate sector as a whole. 
    For homebuyers:
    Increased security: The escrow account requirement ensures that buyers' funds are used for the intended purpose, reducing the risk of fraud and financial mismanagement.
    Protection against delays: Timely project delivery is enforced, and buyers are compensated for delays.
    Enhanced transparency: Access to all project details, including legal and financial information, allows buyers to make informed decisions.
    Efficient dispute resolution: A fast-track mechanism provides a clear path for resolving grievances against developers. 
    For developers:
    Increased credibility: By complying with RERA, developers can build trust and credibility in the market, attracting more genuine buyers and investors.
    Market stability: The regulatory framework brings stability to the market and can attract more domestic and foreign investment.
    Professionalism: The act promotes ethical and professional conduct within the industry. 

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


    annexes_chunks = ""
    recitals_chunks = ""
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
