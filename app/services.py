import datetime
import logging

import pinecone
from langchain.docstore.document import Document

from app import models, settings, utils

logger = logging.getLogger(__name__)


def generate_change_log(since):
    git_client = utils.get_git_client()

    desc_chain = models.get_chain_for_changelog_description()
    bp_chain = models.get_chain_for_changelog_bullet_points()

    commit_messages = git_client.get_commits(since=since)

    description = desc_chain.run(commit_messages)
    bullet_points = bp_chain.run(commit_messages)
    return f"""
## Product Updates - {datetime.datetime.now().strftime("%d/%m/%Y")}

### Description
{description}

### Bullet points
{bullet_points}
```
"""


def generate_code_report(framework):
    git_client = utils.get_git_client()

    files = git_client.get_files()

    chain_raw = models.get_chain_for_code_report_single_file()
    chain_file = models.get_chain_for_code_report_single_file_refactored()

    files = utils.filter_files(files, framework)

    results = []
    for file in files:
        try:
            file_content = git_client.get_file_content(file_path=file["path"])
            improvements = chain_raw.run(file_path=file["path"], content=file_content)
            result_file = chain_file.run(
                file_path=file["path"], content=file_content, improvements=improvements
            )
            results.extend(
                (
                    f"{file['path']} \n {improvements}",
                    f"{file['path']} \n {result_file}",
                )
            )
            print(f"{file['path']} \n {improvements} \n {result_file}")
        except Exception as e:
            logger.error(f"Error while running chain for {file['path']}: {e}")

    results = "\n".join(results)
    with open(
        f"./reports/report_{datetime.datetime.now().strftime('%Y-%m-%d')}.md", "w"
    ) as f:
        f.write(results)
    return results


def comment_pull_requests():
    git_client = utils.get_git_client()
    chain_code = models.get_chain_for_code_assistant()
    pull_requests = git_client.get_pull_requests()

    for pr in pull_requests:
        if git_client.can_comment(pr):
            changes = "\n".join(
                [change["diff"] for change in git_client.get_pull_request_changes(pr)]
            )
            try:
                message = chain_code.run(changes=changes)
                git_client.comment_pull_request(pr, message)
            except Exception as e:
                logger.error(f"Error while running chain {e}")


def file_exists(file_path):
    index = pinecone.Index(settings.PINECONE_INDEX_NAME)
    fetch_response = index.query(
        vector=[0 for i in range(1536)],
        top_k=10,
        namespace="",
        filter={"file_path": file_path},
        include_values=True,
        include_metadata=True,
    )
    return len(fetch_response["matches"]) > 0


def index_code_base():
    vectorstore = models.get_vectorstore()
    git_client = utils.get_git_client()
    files = git_client.get_files()

    filtered_files = utils.filter_files(files, "django")

    for file in filtered_files:
        file_content = git_client.get_file_content(file_path=file["path"])
        file_content = f"{file['path']} \n {file_content}"
        doc = Document(page_content=file_content, metadata={"file_path": file["path"]})

        if not file_exists(file["path"]):
            try:
                vectorstore.add_texts([doc.page_content], [doc.metadata])
                logger.info(f"Indexed file {file['path']}.")
            except Exception as e:
                logger.error(f"Error while indexing file {file['path']}: {e}")

    logger.info("Indexed all the codebase.")


def generate_response(question):
    vectorstore = models.get_vectorstore()
    docs = vectorstore.similarity_search(
        question, search_distance=settings.SEARCH_DISTANCE
    )
    docs = utils.reduce_number_of_docs(docs[:5])
    files = "\n".join([doc.page_content for doc in docs])
    chain = models.get_chain_for_developer_copilot()
    return chain.run(files=files, question=question)
