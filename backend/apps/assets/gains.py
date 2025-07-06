from decimal import Decimal
from typing import Iterable, List, Tuple

from .models import Asset

TransactionData = Tuple[Decimal, Decimal]


def calculate_gain(
    transactions: Iterable[TransactionData], strategy: str = "fifo"
) -> Decimal:
    """Compute realised gain for a series of (quantity, price) pairs."""
    inventory: List[dict[str, Decimal]] = []
    gain = Decimal("0")
    for qty, price in transactions:
        qty = Decimal(qty)
        price = Decimal(price)
        if qty > 0:
            inventory.append({"qty": qty, "price": price})
        else:
            qty_to_sell = -qty
            while qty_to_sell > 0 and inventory:
                if strategy == "lifo":
                    lot = inventory[-1]
                elif strategy == "max":
                    lot = max(inventory, key=lambda item: price - item["price"])
                else:  # fifo
                    lot = inventory[0]
                use = min(qty_to_sell, lot["qty"])
                gain += (price - lot["price"]) * use
                lot["qty"] -= use
                qty_to_sell -= use
                if lot["qty"] == 0:
                    inventory.remove(lot)
    return gain


def gain_for_asset(asset: Asset, strategy: str = "fifo") -> Decimal:
    """Calculate realised gain for an Asset based on linked transactions."""
    links = asset.assettransactionlink_set.select_related("transaction").order_by(
        "transaction__created_at"
    )
    pairs: List[TransactionData] = []
    for link in links:
        price = link.transaction.amount
        pairs.append((link.quantity, price))
    return calculate_gain(pairs, strategy)
