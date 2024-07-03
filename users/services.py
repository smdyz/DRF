import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def converter_USD_in_RUB(amount: float) -> int:
    """Конвертер валюты в рубли"""

    currency_converter = CurrencyRates()
    rate = currency_converter.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_product_with_price(name: str, currency: str = "usd", unit_amount: int = 0) -> stripe.Price:
    """
    Create a product in Stripe.
    :param unit_amount:
    :param currency:
    :param str name: Product name
    """
    product = stripe.Product.create(name=name)
    price = stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount * 100,
        product_data={"name": product["name"]},
    )
    return price


def create_stripe_session(price: stripe.Price) -> tuple:
    """
    Create a Stripe session.
    """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
