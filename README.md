# Kosuke

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
    --framework {framework}
    --date {date}

Frameworks currently supported:

- `django` 

Provide date in the following format

- ``

## Demo

You can check how the bot works here:

https://user-images.githubusercontent.com/29598954/220421332-545419de-bd2e-4fb4-9805-50ee77f184c2.MP4

## License

This project is licensed under the MIT License.
