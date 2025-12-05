#Адрес кошелька: kQAt0aLhmSgN6mnaovSSCTS8z4f5m_7Ov-9S-5NyQTK6l_8o
from tonsdk.contract.wallet import Wallets, WalletVersionEnum


mnemonics = ['lens', 'abuse', 'maze', 'trigger', 'spy', 
             'isolate', 'admit', 'ill', 'divorce', 'use', 
             'nature', 'day', 'true', 'park', 'fee', 'alpha', 
             'drip', 'there', 'motion', 'lawsuit', 'portion', ''
             'clump', 'wine', 'bounce']

mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)

wallet_address = wallet.address.to_string(True, True, True, True)

print(wallet_address)