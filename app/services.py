import datetime
import logging

from app import models, settings, utils

logger = logging.getLogger(__name__)


def generate_change_log(since):
    gitlab_client = utils.get_gitlab_client()

    desc_chain = models.get_chain_for_changelog_description()
    bp_chain = models.get_chain_for_changelog_bullet_points()

    commit_messages = gitlab_client.get_project_commits(since=since)

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
    gitlab_client = utils.get_gitlab_client()

    files = gitlab_client.get_project_files()
    project = gitlab_client.get_project()

    chain_raw = models.get_chain_for_code_report_single_file()
    chain_file = models.get_chain_for_code_report_single_file_refactored()

    files = utils.filter_files(files, framework)

    results = []
    for file in files:
        try:
            file_content = project.files.get(
                file_path=file["path"], ref=project.default_branch
            ).decode()
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


def get_latest_comment_date(mr):
    latest_comment_date = None
    for comment in mr.notes.list():
        comment_date = datetime.datetime.strptime(
            comment.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if not latest_comment_date or comment_date > latest_comment_date:
            latest_comment_date = comment_date
    return latest_comment_date


def get_latest_commit_date(mr):
    latest_commit_date = None
    for commit in mr.commits():
        commit_date = datetime.datetime.strptime(
            commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if not latest_commit_date or commit_date > latest_commit_date:
            latest_commit_date = commit_date
    return latest_commit_date


def can_comment(mr):
    comments = mr.notes.list()
    if comments:
        latest_comment_date = get_latest_comment_date(mr)
        latest_commit_date = get_latest_commit_date(mr)
        return latest_commit_date > latest_comment_date
    else:
        return True


def comment_merge_requests():
    chain_code = models.get_chain_for_code_assistant()

    gitlab_client = utils.get_gitlab_client()
    project = gitlab_client.get_project()

    merge_requests = project.mergerequests.list(
        target_branch=gitlab_client.branch_name, state="opened"
    )

    for mr in merge_requests:
        if can_comment(mr):
            changes = "\n".join([change["diff"] for change in mr.changes()["changes"]])
            message = chain_code.run(changes=changes)
            mr.notes.create({"body": f"# {settings.BOT_NAME} Says \n {message}"})
