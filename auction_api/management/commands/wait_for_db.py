import sys
import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = (
        "Wait for the database to be ready before executing further commands. "
        "Use --poll_seconds to set the interval between retries "
        "and --max_retries to limit the number of attempts."
    )

    def add_arguments(self, parser):
        parser.add_argument("--poll_seconds", type=float, default=3)
        parser.add_argument("--max_retries", type=int, default=15)

    def handle(self, *args, **options):
        max_retries = options["max_retries"]
        poll_seconds = options["poll_seconds"]

        self.stdout.write(
            f"Waiting for database... Poll every {poll_seconds}s, max retries: {max_retries}"
        )

        for retry in range(max_retries):
            try:
                connection.ensure_connection()
            except OperationalError as ex:
                self.stdout.write(
                    "Database unavailable on attempt {attempt}/{max_retries}:"
                    " {error}".format(
                        attempt=retry + 1,
                        max_retries=max_retries,
                        error=ex,
                    )
                )
                time.sleep(poll_seconds)
            else:
                self.stdout.write(self.style.SUCCESS(f"Database ready!"))
                break
        else:
            self.stdout.write(self.style.ERROR("Database unavailable"))
            sys.exit(1)
