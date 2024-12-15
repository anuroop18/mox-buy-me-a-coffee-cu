from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE
RANDOM_USER = boa.env.generate_address("non-owner")
TEN_RANDOM_USERS = [boa.env.generate_address(f"non-owner-{i}") for i in range(10)]

def test_price_feed_is_correct(coffee, eth_usd_pricefeed):
    assert coffee.PRICE_FEED() == eth_usd_pricefeed.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_fund_fails_if_not_enough_eth(coffee, account):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE*10)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE
        
def test_non_owner_cannot_withdraw(coffee_funded):
    # Act
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()
        
def test_owner_can_withdraw(coffee_funded):
    # Act
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    # Assert
    assert boa.env.get_balance(coffee_funded.address) == 0
    # assert coffee_funded.funders == [] # TODO: fix this
    assert coffee_funded.funder_to_amount_funded(coffee_funded.OWNER()) == 0

# Doesn't work with eravm.. so gas related issues in assertion maybe.
def test_multiple_funds_and_withdraw(coffee, account):
    # Starting balance of owner
    STARTING_OWNER_BALANCE = boa.env.get_balance(coffee.OWNER())
    # Arrange
    # Set balance of TEN_RANDOM_USERS
    for user in TEN_RANDOM_USERS:
        boa.env.set_balance(user, SEND_VALUE*10)

    # Calculate the total balance of the funders
    TOTAL_FUNDED = 10*SEND_VALUE
    # Act
    # Fund the contract with 10 different users
    for user in TEN_RANDOM_USERS:
        with boa.env.prank(user):
            coffee.fund(value=SEND_VALUE)

    total_coffee_balance_before_withdraw = boa.env.get_balance(coffee.address)
    print(f"Total balance of coffee before withdraw: {total_coffee_balance_before_withdraw}")
    # Withdraw the contract using the owner
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()
    # Assert
    # Check that the contract has 0 balance
    assert boa.env.get_balance(coffee.address) == 0
    # Check that the funder_to_amount_funded mapping is empty
    for user in TEN_RANDOM_USERS:
        assert coffee.funder_to_amount_funded(user) == 0
    # Check that the balance of the owner is the sum of the balances of the funders
    assert boa.env.get_balance(coffee.OWNER()) == STARTING_OWNER_BALANCE + TOTAL_FUNDED

def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0