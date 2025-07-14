from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from app.models.llm import llm

llm_intent = llm.with_structured_output(UserIntent)

Analyzer_prompt = ChatPromptTemplate.from_messages([
    ("system", classification_few_shot_prompt_examples),
    ("user", "{input}")
])
Analyzer_chain = Analyzer_prompt | llm_intent