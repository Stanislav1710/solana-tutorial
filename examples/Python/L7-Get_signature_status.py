from solana.rpc.api import Client
from solders.signature import Signature


client = Client("https://api.devnet.solana.com")

signatures = [
    Signature.from_string("Qu7MpMvUeY7jDUB1F8LhiDQqckFH3p6BdDP69MEFMdSf7tk6NZiU8Em83F26tr9tHMy1woxwx12ohdeTvJAWQHm"),
    Signature.from_string("3hKzDKm7aJhQKD3F55sa1DTJkxQ3VGdrw5tSJ63gLkhRx2xYctdW4gPam91ttqofLFqAEjW1GghqKrmxvjZPUBqk"),
    Signature.from_string("A4YregcmZLG6gmtwF87THMzhcygp2EZyR7Fz5NYyQQutdizxcXjZu8AVKKxQnen56C5XLvPskts244M1jFh8be2")
]

resp = client.get_signature_statuses(signatures)

for i, s in enumerate(resp.value):
    sig = signatures[i]
    print(f"\nСигнатура {i + 1}: {sig}")

    if s is None:
        print("  Статус не найден (возможно, транзакция слишком старая)")
        continue

    print("  Slot:", s.slot)
    print("  Confirmations:", s.confirmations)
    print("  Status:", s.status)
    print("  Err:", s.err)
    print("  Confirmation status:", s.confirmation_status)
