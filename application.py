"""
AWS Elastic Beanstalk entry point
This file is required by Elastic Beanstalk to start the application
"""
from backend.app import app as application

# Elastic Beanstalk looks for an 'application' object
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)
