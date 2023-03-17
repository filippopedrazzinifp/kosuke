import tiktoken

from app.clients import gitlab
from app import settings


def get_gitlab_client():
    return gitlab.GitlabClient(
        settings.GITLAB_ACCESS_TOKEN,
        settings.GITLAB_PROJECT_NAME,
        settings.GITLAB_BRANCH_NAME,
    )


def filter_files(files, framework):
    if framework == "django":
        exclude_patterns = ["__init__.py", "settings", "urls.py",
                            "wsgi.py", "asgi.py", "manage.py", "apps.py", "websocket", "celery", "migrations"]
        return [
            file
            for file in files
            if all(pattern not in file["path"] for pattern in exclude_patterns)
        ]
    return files
