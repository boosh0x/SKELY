from contracts import skely_token
from eth_utils import to_wei
from moccasin.boa_tools import VyperContract


INITIAL_SUPPLY = to_wei(1000, "ether")


def deploy():
    skely_contract = skely_token.deploy(INITIAL_SUPPLY)
    print(f"Deployed to {skely_token.address}")
    return skely_contract


def moccasin_main() -> VyperContract:
    return deploy()
