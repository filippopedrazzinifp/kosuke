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

# General
# ------------------------------------------------------------------------------
BOT_NAME=
```

2. Run the app with `docker-compose`

```bash
docker-compose up --build -d
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

## License

This project is licensed under the MIT License.

## Example Usage

    python main.py --task analyze --framework django

    python main.py --task index_code_base

    python main.py --task init_pinecone

    python main.py --task chat --question "How can I optimize my database queries?"

    python main.py --task code_review

## Roadmap & Ideas

* Automated testing and bug tracking (merge request)
    * Automatically create test cases
    * Automatically check for bugs
* Extract design guidelines from Picture
* Build a landing page with Ghost
* Update the documentation based on the commits - define the default framework. Read the docs?
* Fine tune using tickets and code
* Build Django auth with chatgpt
* Code migration
    * Translate a codebase from one framework to another one

- Security analysis: Kosuke could be extended to perform security analysis on code, including checking for common vulnerabilities and suggesting improvements to prevent attacks.
- Code refactoring: Kosuke could be used to help refactor code, including identifying redundant or poorly structured code and suggesting better alternatives.
- Code optimization: In addition to suggesting algorithmic improvements, Kosuke could help optimize code for performance and resource usage by identifying areas of code that are particularly resource-intensive.
- Code generation: Kosuke could be used to generate code based on natural language descriptions or user input, potentially helping developers automate repetitive tasks.
- Documentation translation: Kosuke could be used to automatically translate code documentation into multiple languages, making it easier for teams working in different countries or regions to collaborate.
- Machine learning integration: Kosuke could be integrated with machine learning frameworks to help developers build and train machine learning models more easily, potentially including automatic feature selection and parameter tuning.
- Code style enforcement: Kosuke could be used to enforce code style guidelines, potentially including checking for indentation, naming conventions, and other best practices.
- Real-time code review: Kosuke could be integrated with code editors to provide real-time feedback and suggestions as developers write code, helping catch errors and improve code quality as it's being written.
- Code similarity analysis: Kosuke could be used to identify code that is similar or identical across different parts of a codebase, potentially helping reduce redundancy and improve maintainability.
- Integration with testing frameworks: Kosuke could be integrated with popular testing frameworks to help generate test cases and identify areas of code that are particularly prone to errors.
- Integration with project management tools: Kosuke could be integrated with project management tools like Jira or Trello to help manage tasks and track progress.
