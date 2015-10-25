#!/usr/bin/env python
import os
import sys
#import psycopg2

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corazon.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
