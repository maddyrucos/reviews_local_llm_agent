from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from rag import Retriever

class Model:
    def __init__(self):
        self.model = OllamaLLM(model="llama3.2")
        self.template = """
        You are an expert in answering questions about a pizza restaurant

        Here are some relevant reviews: {reviews}

        Here is the question to answer: {question}
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def answer_question(self, question, reviews):
        result = self.chain.invoke({"reviews": reviews, "question": question})
        return result
