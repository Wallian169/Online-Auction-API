from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from auction_api.tasks import close_auction_lots


class Command(BaseCommand):
    help = "Run the APScheduler"

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_job(close_auction_lots, "interval", minutes=1)
        scheduler.start()
        self.stdout.write("Scheduler started. Running jobs...")

        try:
            while True:
                pass  # Keeps the scheduler alive
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
