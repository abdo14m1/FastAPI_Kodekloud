import gunicorn.app.base
from app.main import app
from app.config import CERT_FILE, KEY_FILE, HOST, PORT, WORKERS

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        'bind': f'{HOST}:{PORT}',
        'workers': WORKERS,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'certfile': str(CERT_FILE),
        'keyfile': str(KEY_FILE),
        # Production settings
        'accesslog': '-',  # Log to stdout
        'errorlog': '-',   # Log to stdout
        'worker_connections': 1000,
        'timeout': 30,
        'keepalive': 2,
        'backlog': 2048,
    }

    StandaloneApplication(app, options).run()
