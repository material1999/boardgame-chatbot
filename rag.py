import requests
import yaml
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.schema import Document


def load_credentials(path="./credentials.yml"):
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def generate_groq_text(user_query):

    grok_api_key = load_credentials().get("grok", {}).get("api_key")

    system_prompt = ("You are a board game chatbot and you have to answer user questions about the rulebooks."
                     "You will be also given some help from an external knowledge source as part of the user prompt,"
                     "please use the provided information to answer user questions. If it is provided,"
                     "feel free to include exact references from the rulebook (page numbers, quotes, etc)."
                     "In your answer, don't write down if some information came from the external source."
                     )

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {grok_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": user_query}],
                "temperature": 0.7,
                "max_tokens": 200
            }
        )

        data = response.json()
        message = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        if not message:
            return "No response generated from the API."

        return message

    except Exception as e:
        return f"Error generating text: {str(e)}"


def create_prompt(user_query):
    loader = TextLoader("./data/txt/terraforming_mars.txt")
    document = loader.load()

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = InMemoryVectorStore(embedding=embedding_model)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    docs = text_splitter.split_documents(document)

    # text_splitter = SemanticChunker(embeddings=embedding_model)
    # docs = text_splitter.split_documents(document)

    docs = [
        Document(page_content=doc.page_content.replace('\n', ' '), metadata=doc.metadata)
        for doc in docs
    ]

    vector_store.add_documents(documents=docs)

    results = vector_store.similarity_search(
        query=user_query,
        k=10,
    )

    prompt_string = user_query + "\n#####\nExternal knowledge:\n"

    for res in results:
        prompt_string += f"--- {res.page_content}\n"
        # print(f"--- {res.page_content}")
    prompt_string += "#####\n"

    return prompt_string


# user_query = "How many players can play the game?"
# user_query = "How to win?"
user_query = "Can you play solo?"

# print(generate_groq_text(user_query))

user_query = create_prompt(user_query)
print(user_query)
print(generate_groq_text(user_query))
