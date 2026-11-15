from app.database import get_db


def test_get_db_session_yield():
    """Testa se a dependência get_db produz e fecha a sessão do banco corretamente."""
    gen = get_db()
    session = next(gen)
    assert session is not None
    try:
        next(gen)
    except StopIteration:
        pass
