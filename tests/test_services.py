from unittest.mock import Mock

from app import models, services

models.get_chain_for_code_report_single_file = Mock()
models.get_chain_for_code_report_single_file.run.return_value = "Hello"

models.get_chain_for_code_report_single_file_refactored = Mock()
models.get_chain_for_code_report_single_file_refactored.run.return_value = "Hello"

models.get_chain_for_code_assistant = Mock()
models.get_chain_for_code_assistant.run.return_value = "Hello"


def test_comment_pull_requests():
    services.comment_pull_requests()


def test_generate_code_report():
    services.generate_code_report("django")


def test_index_code_base():
    services.index_code_base()
