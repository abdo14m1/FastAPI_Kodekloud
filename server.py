import gunicorn.app.base
from app.main import app
from app.config import Settings

settings = Settings()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        "bind": f"{settings.HOST}:{settings.PORT}",
        "workers": settings.WORKERS,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "certfile": str(settings.SSL_CERT_FILE),
        "keyfile": str(settings.SSL_KEY_FILE),
        # Production settings
        "accesslog": "-",
        "errorlog": "-",
        "worker_connections": 4,
        "timeout": 30,
        "keepalive": 2,
        "backlog": 2048,
    }

    StandaloneApplication(app, options).run()
