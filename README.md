# Kosuke

> Are you a better Software Engineer than ChatGPT?

Kosuke is an asynchronous code assistant. It can perform code reviews, analyze entire codebases and generate descriptive changelogs for marketing purposes.
## Run Locally

### Run with docker-compose

1. Create a `.env` file including the following environment variables

```bash
# OpenAI
# ------------------------------------------------------------------------------
OPENAI_API_KEY=

# GitLab
# ------------------------------------------------------------------------------
GITLAB_ACCESS_TOKEN=
GITLAB_BRANCH_NAME=
GITLAB_RELEASE_BRANCH_NAME=
GITLAB_PROJECT_NAME=

# General
# ------------------------------------------------------------------------------
BOT_NAME=
```

2. Run the app with `docker-compose`

```bash
docker-compose up --build -d
```
## One shot commands available

Run `main.py` with one of the following parameters

    --task {anaylyze|change_log|code_review}
    --framework {django}
    --since_date {%Y-%m-%d}

## Frameworks Currently Supported

- `django`

## License

This project is licensed under the MIT License.

## Example Usage

    python main.py --task analyze --framework django

## Roadmap

- [ ] Index all the files in Pinecone in order to deliver talk to your code use case
- [ ] Index all the project documentation in Pinecone
