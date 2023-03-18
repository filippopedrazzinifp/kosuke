from app import models, settings
from app.clients import gitlab


def get_gitlab_client():
    return gitlab.GitlabClient(
        settings.GITLAB_ACCESS_TOKEN,
        settings.GITLAB_PROJECT_NAME,
        settings.GITLAB_BRANCH_NAME,
    )


def filter_files(files, framework):
    if framework == "django":
        exclude_patterns = [
            "__init__.py",
            "settings",
            "urls.py",
            "wsgi.py",
            "asgi.py",
            "manage.py",
            "apps.py",
            "websocket",
            "celery",
            "migrations",
        ]
        return [
            file
            for file in files
            if all(pattern not in file["path"] for pattern in exclude_patterns)
        ]
    return files


def reduce_number_of_docs(docs):
    num_docs = len(docs)
    tokenizer = models.get_tokenizer()

    tokens = [len(tokenizer.encode(doc.page_content)) for doc in docs]

    token_count = sum(tokens[:num_docs])
    while token_count > settings.OPENAI_MAX_TOKENS:
        num_docs -= 1
        token_count -= tokens[num_docs]

    return docs[:num_docs]
