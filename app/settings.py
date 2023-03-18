import os

from dotenv import load_dotenv

load_dotenv()

# General
# -------------------------------------------------------------------------------
BOT_NAME = os.getenv("BOT_NAME")
FRAMEWORK = os.getenv("FRAMEWORK")

# Gitlab
# -------------------------------------------------------------------------------
GITLAB_ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
GITLAB_PROJECT_NAME = os.getenv("GITLAB_PROJECT_NAME")
GITLAB_BRANCH_NAME = os.getenv("GITLAB_BRANCH_NAME")
GITLAB_RELEASE_BRANCH_NAME = os.getenv("GITLAB_RELEASE_BRANCH_NAME")

# OpenAI
# -------------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MAX_TOKENS = 8000

# Pinecone
# -------------------------------------------------------------------------------
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Search
# -------------------------------------------------------------------------------
SEARCH_DISTANCE = 0.9
