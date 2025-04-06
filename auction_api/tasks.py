from datetime import timedelta

from celery import shared_task
from django.db.models import OuterRef, Subquery
from django.utils.timezone import now


@shared_task
def close_auction_lots():
    from auction_api.models import AuctionLot, Bid

    print("Started closing auction lots...")

    max_bids = Bid.objects.filter(auction_lot=OuterRef("pk")).order_by("-offered_price")

    expired_lots = (
        AuctionLot.objects.filter(close_time__lte=now())
        .prefetch_related("bids")
        .annotate(
            max_bid=Subquery(max_bids.values("offered_price")[:1]),
            found_winner=Subquery(max_bids.values("bidder_id")[:1]),
        )
    )

    if not expired_lots:
        print("No expired auction lots found.")
    else:
        print(f"Found {expired_lots.count()} expired lots to close.")

    lots_to_close = []
    lots_to_delete = []
    for expired_lot in expired_lots:
        print(
            f"Closing lot {expired_lot.id}: " f"Winner id is {expired_lot.found_winner}"
        )
        age = now() - expired_lot.close_time
        if expired_lot.is_active:
            expired_lot.is_active = False
        expired_lot.winner_id = expired_lot.found_winner
        if age > timedelta(days=3):
            print(f"Deleting lot {expired_lot.id} — expired more than 3 days ago.")
            lots_to_delete.append(expired_lot.id)
        lots_to_close.append(expired_lot)

    if lots_to_close:
        AuctionLot.objects.bulk_update(lots_to_close, ["is_active", "winner_id"])
        print(f"Closed {len(lots_to_close)} lots.")

    if lots_to_delete:
        AuctionLot.objects.filter(id__in=lots_to_delete).delete()
        print(f"Deleted {len(lots_to_delete)} lots.")


@shared_task
def test_task():
    print("Task executed!")
    return "Task completed!"
