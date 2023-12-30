FROM python:3.11

RUN pip install "commitizen>=3.12.0,<4.0.0" "cz-github-jira-conventional>=2.0.0,<3.0.0"

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
