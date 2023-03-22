# Kosuke

> Are you a better Software Engineer than ChatGPT?

Kosuke is an asynchronous code assistant that can perform code reviews, analyze entire codebases, and generate descriptive changelogs for marketing purposes. It's designed to help developers improve their code quality and productivity.

## Run Locally

### Run with docker-compose

1. Create a `.env` file including the following environment variables

```bash
# OpenAI
# ------------------------------------------------------------------------------
OPENAI_API_KEY=

# Pinecone
# ------------------------------------------------------------------------------
PINECONE_API_KEY=
PINECONE_INDEX_NAME=

# GitLab
# ------------------------------------------------------------------------------
GITLAB_ACCESS_TOKEN=
GITLAB_BRANCH_NAME=
GITLAB_RELEASE_BRANCH_NAME=
GITLAB_PROJECT_NAME=

# Github
# ------------------------------------------------------------------------------
GITHUB_ACCESS_TOKEN=
GITHUB_PROJECT_NAME=
GITHUB_BRANCH_NAME=
GITHUB_RELEASE_BRANCH_NAME=

# General
# ------------------------------------------------------------------------------
BOT_NAME=
```

2. Run the app with `docker-compose`

```bash
docker-compose up --build -d
```

3. Stop the app

```bash
docker-compose down
```

## One shot commands available

Kosuke provides several one-shot commands that you can use to perform different tasks. Here's a list of available commands:

- `analyze`: analyzes the codebase and provides feedback on potential issues
- `change_log`: generates a descriptive changelog for marketing purposes
- `code_review`: reviews the code and provides suggestions for improvement
- `index_code_base`: indexes the codebase for talk to your code use case
- `init_pinecone`: initializes Pinecone for use with Kosuke
- `chat`: generates a response to a user question based on your indexed codebase

Each command can be run with the following optional parameters:

- `--framework`: specifies the framework used in the codebase (currently only django is supported)
- `--since_date`: specifies the date from which to start the analysis (in the format %Y-%m-%d)

## Frameworks Currently Supported

Kosuke currently supports the `django` framework, which is a popular web framework for Python.

## Example Usage

    python main.py --task analyze --framework django

    python main.py --task index_code_base

    python main.py --task init_pinecone

    python main.py --task chat --question "How can I optimize my database queries?"

    python main.py --task code_review

## License

This project is licensed under the MIT License.
