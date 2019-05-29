from config.config import CodeTemplate, Config
from .client import Client
from .contest import Contest
from .login import get_csrf_token, check_login


def submit(contest: Contest, problem_id: str, source_code: str, template: CodeTemplate) -> None:
    if contest is None or problem_id is None:
        print("[ERROR!] Can't find contest by this id or can't find problem by this problem id")
        return

    client = Client()
    session = client.get_session()
    cfg = Config()
    url = contest.get_url() + '/submit'

    resp = session.get(url)

    if not check_login(resp.text, client.username):
        cfg.login()
        resp = session.get(url)
    csrf = get_csrf_token(resp.text)
    with open(source_code) as f:
        code = f.read()

    print(f"Submiting in contest {contest.id} problem {problem_id}.")
    session.post(url, data={
        "csrf_token": csrf,
        "ftaa": client.ftaa,
        "bfaa": client.bfaa,
        "action": "submitSolutionFormSubmitted",
        "programTypeId": template.lang.id,
        "submittedProblemIndex": problem_id,
        "source": code,
        "tabSize": 4,
        "_tta": 594,
        "sourceCodeConfirmed": True
    })
