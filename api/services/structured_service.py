from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from api.core.config import settings
from api.core.logging import logger

class MobileFeatureStructure(BaseModel):
    """Structure for explaining mobile app features"""
    feature_purpose: str = Field(description="Brief explanation of what this feature does")
    how_to_access: str = Field(description="How to find and access this feature in the mobile app")
    key_steps: List[str] = Field(description="Step-by-step instructions")
    usage_tips: List[str] = Field(description="1-3 practical tips for effective use")
    related_features: Optional[List[str]] = Field(default=None, description="Other related features that might be useful")

def get_structured_output(question: str, context: Optional[str] = None) -> MobileFeatureStructure:
    try:
        parser = PydanticOutputParser(pydantic_object=MobileFeatureStructure)
        
        if context:
            template = """
            You are a helpful Simpro Mobile app guide providing clear, concise information for users on the go.
            
            CONTEXT INFORMATION:
            {context}
            
            Based on the context above, explain the feature in the following question in a mobile-friendly, structured format:
            {question}
            
            Focus on clarity and brevity - users are viewing this on a mobile device.
            
            {format_instructions}
            """
            prompt = PromptTemplate(
                template=template,
                input_variables=["question", "context"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            input_data = {"question": question, "context": context}
        else:
            template = """
            You are a helpful Simpro Mobile app guide providing clear, concise information for users on the go.
            
            Please explain the feature in the following question in a mobile-friendly, structured format:
            {question}
            
            Focus on clarity and brevity - users are viewing this on a mobile device.
            
            {format_instructions}
            """
            prompt = PromptTemplate(
                template=template,
                input_variables=["question"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            input_data = {"question": question}
        
        llm = OpenAI(temperature=settings.LLM_TEMPERATURE)
        chain = prompt | llm | parser
        
        return chain.invoke(input_data)
    except Exception as e:
        logger.error(f"Error generating structured output: {str(e)}")
        return MobileFeatureStructure(
            feature_purpose="Sorry, I couldn't retrieve information about this feature.",
            how_to_access="Please try asking about a different feature or rephrase your question.",
            key_steps=["N/A"],
            usage_tips=["Try asking about specific SimPro mobile features like 'mobile audit' or 'time sheets'"]
        )