from solana.rpc.api import Client
from solders.signature import Signature

client = Client("https://api.mainnet-beta.solana.com")

sig = Signature.from_string("4XFbY13NfM2DM65BtWY88mTUMqX49kdPQXD77fPUftYdcA5djysST77dNsA6jGdiEgqvMrkWVENhjETS8szTJcFA")
resp = client.get_signature_statuses([sig])
status = resp.value[0]

if status is None:
    print("Статус: не найден (вероятно, старый и очищен RPC)")
else:
    print("Результат:", "Ok(())" if status and status.err is None else f"Err({status.err})")
    print("Уровень:", status.confirmation_status)
