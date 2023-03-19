from app import models, settings
from app.clients import github, gitlab


def get_gitlab_client():
    return gitlab.GitlabClient(
        settings.GITLAB_ACCESS_TOKEN,
        settings.GITLAB_PROJECT_NAME,
        settings.GITLAB_BRANCH_NAME,
    )


def get_github_client():
    return github.GithubClient(
        settings.GITHUB_ACCESS_TOKEN,
        settings.GITHUB_PROJECT_NAME,
        settings.GITHUB_BRANCH_NAME,
    )


def get_git_client():
    if settings.GITLAB_ACCESS_TOKEN is not None:
        return get_gitlab_client()
    elif settings.GITHUB_ACCESS_TOKEN is not None:
        return get_github_client()
    else:
        raise ValueError("No git client configured")


def filter_files(files, framework):
    python_files = [f for f in files if f["path"].endswith(".py")]
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
            for file in python_files
            if all(pattern not in file["path"] for pattern in exclude_patterns)
        ]
    return python_files


def reduce_number_of_docs(docs):
    num_docs = len(docs)
    tokenizer = models.get_tokenizer()

    tokens = [len(tokenizer.encode(doc.page_content)) for doc in docs]

    token_count = sum(tokens[:num_docs])
    while token_count > settings.OPENAI_MAX_TOKENS:
        num_docs -= 1
        token_count -= tokens[num_docs]

    return docs[:num_docs]
