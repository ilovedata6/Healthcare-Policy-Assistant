from app.config import settings

def test_settings_loaded():
    assert settings.OPENAI_API_KEY is not None
    assert settings.CHUNK_SIZE > 0
