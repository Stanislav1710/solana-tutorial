from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message


client = Client("https://api.devnet.solana.com")

sender = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1000))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), rbh)

tx = Transaction([sender], msg, rbh)
tx.partial_sign([sender], rbh)
resp = client.send_transaction(tx)

sig = resp.value
print("Подпись транзакции:", sig)

st = client.get_signature_statuses([sig]).value[0]
if st is None:
    print("Статус: не найден (слишком старая/не прошла preflight/ещё в кеше RPC)")
else:
    print("Slot:", st.slot)
    print("Confirmations:", st.confirmations)
    print("Err:", st.err)
    print("Confirmation status:", st.confirmation_status)
    print("Результат:", "Ok(())" if st and st.err is None else f"Err({st.err})")
