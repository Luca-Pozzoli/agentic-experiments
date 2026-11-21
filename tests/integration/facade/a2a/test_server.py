from starlette.testclient import TestClient


def test_facade_exposes_agent_card(client_fixture: TestClient) -> None:
    model_card: dict = client_fixture.get("/.well-known/agent-card.json").json()
    assert model_card is not None
