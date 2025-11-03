"""
Application entry point (Assignment requirement: python3 app.py)
This file is required by the assignment specifications.
Runs the Flask development server.
"""

import os
from app import create_app

if __name__ == '__main__':
    # Get config from environment or default to development
    config = os.getenv('FLASK_ENV', 'development')
    
    # Create and run app
    app = create_app(config)

    # On Windows, the Werkzeug reloader causes process handling issues:
    # - With `conda run`, the parent exits immediately (exit code 1)
    # - The reloader spawns child processes that don't clean up properly
    # Disable by default on Windows. Override: FLASK_USE_RELOADER=1
    is_debug = (config == 'development')
    is_windows = os.name == 'nt'
    env_override = os.getenv('FLASK_USE_RELOADER')
    
    if env_override is not None:
        use_reloader = env_override == '1'
    else:
        # Disable reloader on Windows by default to avoid process issues
        use_reloader = is_debug and not is_windows

    try:
        app.run(
            debug=is_debug,
            use_reloader=use_reloader,
            host='0.0.0.0',
            port=5000,
        )
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        pass
