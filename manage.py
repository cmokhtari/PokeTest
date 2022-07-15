#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import coverage


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PokeTest.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    is_testing = 'test' in sys.argv
    if is_testing:
        # If the command is python manage.py test begin launch coverage
        cov = coverage.coverage(
            source=[
                'PokeTest',
                'api_app',
            ],
            omit=[
                '*/migrations/*',
                '*/asgi.py',
                '*/wsgi.py'
            ]
        )
        cov.set_option('report:show_missing', True)
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
        cov.xml_report()


if __name__ == '__main__':
    main()