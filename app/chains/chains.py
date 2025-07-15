
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.models.llm import llm
from app.models.models import Log_analysis, Network_design, Server_manager
from app.prompts.prompts import analyzer_prompt_template
from app.prompts.prompts import network_designer_prompt_template 
from app.prompts.prompts import server_manager_prompt_template


llm_analyzer = llm.with_structured_output(Log_analysis)
llm_network_design = llm.with_structured_output(Network_design)
llm_server_manager = llm | StrOutputParser()


def get_analyzer_chain():
    analyzer_prompt = ChatPromptTemplate.from_messages([
        ("system", analyzer_prompt_template),
        ("user", "{logs}")
    ])

    return analyzer_prompt | llm_analyzer

def get_network_designer_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", network_designer_prompt_template),
        ("user", "{query}")
    ])
    return prompt | llm_network_design

def get_server_manager_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", server_manager_prompt_template),
        ("user", "{query}")
    ])
    return  prompt | llm_server_manager 
