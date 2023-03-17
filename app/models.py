import tiktoken
from langchain.chains import LLMChain
from langchain.docstore.document import Document
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter


def get_tokenizer():
    return tiktoken.get_encoding("cl100k_base")


def get_openai_llm():
    return OpenAIChat(model_name="gpt-4", temperature=0)


def preprocess_text(text):
    text_splitter = TokenTextSplitter()
    texts = text_splitter.split_text(text)
    return [Document(page_content=t) for t in texts]


def get_chain_for_changelog_description():
    llm = get_openai_llm()
    prompt = PromptTemplate(
        input_variables=["commit_messages"],
        template="Generate changelog description for marketing newsletter given the following commit messages: {commit_messages}",  # noqa E501
    )
    return LLMChain(llm=llm, prompt=prompt)


def get_chain_for_changelog_bullet_points():
    llm = get_openai_llm()
    prompt = PromptTemplate(
        input_variables=["commit_messages"],
        template="Summarize in 10 bullet points the following commit messages for a marketing report: {commit_messages}",  # noqa E501
    )
    return LLMChain(llm=llm, prompt=prompt)


def get_chain_for_code_report_single_file():
    template = """
    You are a code assistant. Your objective is to improve code quality, discover potential bugs, and suggest improvements. # noqa E501
    You are given the following file and raw content.

    File: {file_path}
    =========
    Content: {content}
    =========
    Return the answer in bullet points. IMPORTANT: write only the most critical and most important improvements. If there are not critical problems or improvements, just return an empty string. # noqa E501
    """
    prompt = PromptTemplate(
        input_variables=["file_path", "content"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def get_chain_for_code_report_single_file_refactored():
    template = """
    Given the following file content, refactor the code based on the improvements suggested by the code assistant. # noqa E501

    File: {file_path}
    =========
    Content: {content}
    =========
    Improvements: {improvements}
    =========

    Return the rewritten file.
    """
    prompt = PromptTemplate(
        input_variables=["file_path", "content", "improvements"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def get_chain_for_code_report():
    template = """
    Generate a code report based on the following content:

    Content: {content}
    =========
    Generate the answer in markdown format.
    """
    prompt = PromptTemplate(
        input_variables=["content"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def get_chain_for_code_assistant_with_file():
    template = """
    You are a code assistant. Your objective is to improve code quality, discover potential bugs, and suggest improvements. # noqa E501
    You are given the following changes of a merge request and the corresponding new file:

    New File: {file_content}
    =========
    Changes: {changes}
    =========

    Provide suggestions in order to adress the most critical issues and improve performances. # noqa E501
    """
    prompt = PromptTemplate(
        input_variables=["changes", "file_content"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def get_chain_for_code_assistant():
    template = """
    You are a code assistant. Your objective is to improve code quality, discover potential bugs, and suggest improvements. # noqa E501
    You are given the following changes of a merge request and the corresponding new file:

    Changes: {changes}
    =========

    Provide suggestions in order to adress the most critical issues and improve performances. # noqa E501
    """
    prompt = PromptTemplate(
        input_variables=["changes"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)


def get_chain_for_summarization():
    template = """
    You are a code assistant. Summarize the following improvements in order to fit in a merge request comment. # noqa E501

    Improvements: {improvements}
    """
    prompt = PromptTemplate(
        input_variables=["improvements"],
        template=template,
    )
    llm = get_openai_llm()
    return LLMChain(llm=llm, prompt=prompt, verbose=True)
