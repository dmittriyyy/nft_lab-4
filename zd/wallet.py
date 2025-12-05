from tonsdk.contract.wallet import Wallets, WalletVersionEnum


mnemonics = ['path', 'tiny', 'ill', 'album', 'surround', 'media', 'evolve', 'nothing', 'more', 'tornado', 'photo', 'license', 'chicken', 'tornado', 'flower', 'follow', 'timber', 'remind', 'afford', 'earth', 'actor', 'area', 'move', 'clever']


mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)

wallet_address = wallet.address.to_string(True, True, True, True)

print(wallet_address)