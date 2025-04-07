class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False