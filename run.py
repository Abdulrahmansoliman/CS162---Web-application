"""
Application entry point
Runs the Flask development server
"""

import os
from app import create_app

if __name__ == '__main__':
    # Get config from environment or default to development
    config = os.getenv('FLASK_ENV', 'development')
    
    # Create and run app
    app = create_app(config)
    app.run(debug=(config == 'development'), host='0.0.0.0', port=5000)
