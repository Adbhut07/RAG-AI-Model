from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="gemma3")

template = """
You are an expert assistant specializing in software engineering documentation, build processes, and development tools.

Based on the following relevant documents, provide accurate and helpful answers to the user's questions.

RELEVANT DOCUMENTATION:
{context}

USER QUESTION: {question}

INSTRUCTIONS FOR RESPONSE:
1. First, carefully review the provided documentation to see if it contains information relevant to the question
2. If the documentation contains relevant information, provide a detailed answer based on that content
3. If the documentation doesn't contain specific information about the question, clearly state this and provide general guidance if possible
4. Always be specific and cite information from the documents when available
5. For build/installation questions, provide step-by-step instructions when available in the documentation

ANSWER:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
a
def format_docs(docs):
    """Format retrieved documents for better context"""
    if not docs:
        return "No relevant documents found."
    
    formatted = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get('source', 'Unknown')
        content = doc.page_content.strip()
        if content:
            formatted.append(f"Document {i+1} (Source: {source}):\n{content}\n")
    
    return "\n".join(formatted)

def main():
    print("RAG Q&A System - Internship Documentation")
    print("Type 'q' to quit")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 50)
        question = input("Ask your question (q to quit): ").strip()
        print()
        
        if question.lower() == "q":
            print("Goodbye!")
            break      
            
        if not question:
            print("Please enter a valid question.")
            continue
        
        try:
            docs = retriever.invoke(question)
            
            context = format_docs(docs)
            
            result = chain.invoke({"context": context, "question": question})
            print(result)
            
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            print("Please try rephrasing your question.")

if __name__ == "__main__":
    main()
