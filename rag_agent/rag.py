from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

class Retriever:
    def __init__(self, model_name="mxbai-embed-large", documents_path="../data/restaurant_reviews.csv"):
        self.df = pd.read_csv(documents_path)
        self.embeddings = OllamaEmbeddings(model=model_name)

        self.db_location = "./chrome_langchain_db"
        self.add_documents = not os.path.exists(self.db_location)

        if self.add_documents:
            self.documents = []
            self.ids = []
            
            for i, row in self.df.iterrows():
                document = Document(
                    page_content=row["Title"] + " " + row["Review"],
                    metadata={"rating": row["Rating"], "date": row["Date"]},
                    id=str(i)
                )
                self.ids.append(str(i))
                self.documents.append(document)
                
        self.vector_store = Chroma(
            collection_name="restaurant_reviews",
            persist_directory=self.db_location,
            embedding_function=self.embeddings
        )

        if self.add_documents:
            self.vector_store.add_documents(documents=self.documents, ids=self.ids)
        
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )

    def invoke(self, question):
        return self.retriever.invoke(question)
