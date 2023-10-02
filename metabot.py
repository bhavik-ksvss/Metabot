# Bunch of inputs
from Metaphor import MetaphorSearch
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

metaphor_api = 'Enter your Metaphor API key here'
open_ai_api = 'Enter your OpenAI API key here'

def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n",'\n', '.', ','],
        chunk_size=4000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #print(len(chunks))
    
    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = OpenAIEmbeddings(openai_api_key = open_ai_api)
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    
    return knowledgeBase

def main():
    keyword = False
    max_retries = 2 # for example, you can set this to any number
    retry_count = 0

    st.title('Ask anything!')
    Metaphor_search = MetaphorSearch(metaphor_api)
    query = st.text_input('Ask a question')
    cancel_button = st.button('Cancel')
    try:
        while retry_count < max_retries:
            if query and isinstance(query, str):
                knowledgeBase = process_text(Metaphor_search.search(query, keyword))
                

                docs = knowledgeBase.similarity_search(query)

                llm = ChatOpenAI(temperature=0.9, openai_api_key=open_ai_api)
                chain = load_qa_chain(llm, chain_type='stuff')

                response = chain.run(input_documents=docs, question=query)

                if 'sorry' in response.lower() or 'i don\'t' in response.lower():
                    keyword = True
                    retry_count += 1
                    continue 
                else:
                    st.write('Response:', response)
                    break  
            else:
                st.write("")
                break
    except Exception as e:
        st.write("")
    
if __name__ == '__main__':
    main()