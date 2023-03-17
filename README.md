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
    code_review: reviews the code and provides suggestions for improvement

Each command can be run with the following optional parameters:

- `--framework`: specifies the framework used in the codebase (currently only django is supported)
- `--since_date`: specifies the date from which to start the analysis (in the format %Y-%m-%d)

## Frameworks Currently Supported

Kosuke currently supports the `django` framework, which is a popular web framework for Python.

## License

This project is licensed under the MIT License.

## Example Usage

    python main.py --task analyze --framework django

## Roadmap

- [ ] Index all the files in Pinecone in order to deliver talk to your code use case
- [ ] Index all the project documentation in Pinecone
- [ ] Support for more programming languages and frameworks
- [ ] Integration with popular code repositories like GitHub and Bitbucket
- [ ] Automated testing and bug tracking
- [ ] Natural language processing to analyze code-related chat or email conversations
- [ ] Accessibility analysis for web applications

## More Ideas

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
