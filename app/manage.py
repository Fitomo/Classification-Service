import os
import config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Set config
app.config.from_object(os.environ['APP_SETTINGS'])

# Setup migrations
migrate = Migrate(app, db)
manager = Manager(app)

# Allow for migration commands from terminal
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
