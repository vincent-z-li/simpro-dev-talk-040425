from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from api.utils.vector_utils import get_vector_store
from api.core.config import settings
from api.core.logging import logger
from api.services.structured_service import get_structured_output

def answer_non_rag(question: str, structured: bool = False) -> dict:
    """Get an answer about mobile features without using RAG."""
    try:
        if structured:
            structured_guide = get_structured_output(question)
            logger.info(f"Non-RAG structured response generated for: {question}")
            return {
                "answer": f"Here's how to use this feature: {structured_guide.feature_purpose}",
                "structured_guide": structured_guide
            }
        
        template = "You are a helpful simpro mobile app assistant. Explain this feature or answer this question about our mobile app: {question}"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm = OpenAI(temperature=settings.LLM_TEMPERATURE)
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.invoke({"question": question})
        
        logger.info(f"Non-RAG question answered about mobile feature: {question}")
        return {"answer": result["text"]}
    except Exception as e:
        logger.error(f"Error in non-RAG answer: {str(e)}")
        raise

def answer_with_rag(question: str, structured: bool = False) -> dict:
    """Get an answer about mobile features using RAG."""
    try:
        vector_store = get_vector_store()
        
        # similarity search to find relevant documents
        docs = vector_store.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        if structured:
            structured_guide = get_structured_output(question, context)
            logger.info(f"RAG structured response generated for: {question}")
            return {
                "answer": f"Here's how to use this feature: {structured_guide.feature_purpose}",
                "structured_guide": structured_guide
            }
        
        prompt_template = """
        You are a simpro mobile app expert helping users understand our SaaS product features.
        Use the following information from our help documents to answer the user's question.
        Make your answer clear, concise and easy to follow on a mobile device.
        
        Context from help documents:
        {context}
        
        User question: {question}
        
        Answer:
        """
        custom_prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        llm = OpenAI(temperature=settings.LLM_TEMPERATURE)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_prompt}
        )
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        
        logger.info(f"RAG question answered about mobile feature: {question}")
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in RAG answer: {str(e)}")
        raise