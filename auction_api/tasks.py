from celery import shared_task
from django.db.models import OuterRef, Subquery
from django.utils.timezone import now


@shared_task
def close_auction_lots():
    from auction_api.models import AuctionLot, Bid

    print("Started closing auction lots...")

    max_bids = Bid.objects.filter(auction_lot=OuterRef("pk")).order_by("-offered_price")

    expired_lots = (
        AuctionLot.objects.filter(is_active=True, close_time__lte=now())
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
    for expired_lot in expired_lots:
        print(
            f"Closing lot {expired_lot.id}: " f"Winner id is {expired_lot.found_winner}"
        )
        expired_lot.is_active = False
        expired_lot.winner_id = expired_lot.found_winner
        lots_to_close.append(expired_lot)

    AuctionLot.objects.bulk_update(expired_lots, ["is_active", "winner_id"])


@shared_task
def test_task():
    print("Task executed!")
    return "Task completed!"
