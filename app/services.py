import logging
import datetime

from app import models, utils, settings

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
    for file in files[0:10]:
        try:
            file_content = project.files.get(file_path=file["path"], ref=project.default_branch).decode()
            improvements = chain_raw.run(file_path=file["path"], content=file_content)
            result_file = chain_file.run(file_path=file["path"], content=file_content, improvements=improvements)
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
    with open("./report.md", "w") as f:
        f.write(results)
    return results


def can_comment(mr):
    comments = mr.notes.list()
    if comments:
        latest_comment = comments[-1]
        latest_comment_date = datetime.datetime.strptime(latest_comment.created_at.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        for commit in mr.commits():
            commit_date = datetime.datetime.strptime(commit.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            if latest_comment_date > commit_date and settings.BOT_NAME in latest_comment.body:
                return False
    return True


def comment_merge_requests(with_new_file=False):
    chain_code = models.get_chain_for_code_assistant()
    chain_code_file = models.get_chain_for_code_assistant_with_file()

    gitlab_client = utils.get_gitlab_client()
    project = gitlab_client.get_project()

    merge_requests = project.mergerequests.list(target_branch=gitlab_client.branch_name, state='opened')

    for mr in merge_requests:
        if can_comment(mr):
            improvements = []
            for change in mr.changes()["changes"]:
                if with_new_file:
                    file_content = project.files.get(file_path=change['new_path'], ref=mr.source_branch).decode()
                    message = chain_code_file.run(changes=change["diff"], file_content=file_content)
                else:
                    message = chain_code.run(changes=change["diff"])
                improvements.append(message)

            improvements = "\n".join(improvements)
            mr.notes.create({'body': f"# {settings.BOT_NAME} Says \n {improvements}"})
