[![PyPI Version](https://badge.fury.io/py/amazon-orders.svg)](https://badge.fury.io/py/amazon-orders)
[![Build](https://github.com/alexdlaird/amazon-orders-python/actions/workflows/build.yml/badge.svg)](https://github.com/alexdlaird/amazon-orders-python/actions/workflows/build.yml)
[![Codecov](https://codecov.io/gh/alexdlaird/amazon-orders-python/branch/main/graph/badge.svg)](https://codecov.io/gh/alexdlaird/amazon-orders-python)
[![Python Versions](https://img.shields.io/pypi/pyversions/amazon-orders.svg)](https://pypi.org/project/amazon-orders/)
[![PyPI License](https://img.shields.io/pypi/l/amazon-orders.svg)](https://pypi.org/project/amazon-orders/)

# Amazon Orders

`amazon-orders` is an unofficial library that provides a command line interface alongside a programmatic API that can
be used to interact with Amazon.com's consumer-facing website.

This works by parsing website data from Amazon.com. A nightly build validates functionality to ensure its
stability, but as Amazon provides no official API to use, this package may break at any time. This
package only supports the English version of the website.

## Installation

`amazon-orders` is available on [PyPI](https://pypi.org/project/amazon-orders/) and can be installed using `pip`:

```sh
pip install amazon-orders
```

That's it! `amazon-orders` is now available as a Python package is available from the command line.

## Basic Usage

Execute `amazon-orders` from the command line with:

```sh
amazon-orders --username <AMAZON_EMAIL> --password <AMAZON_PASSWORD> history
```

Or use `amazon-orders` programmatically:

```python
from amazonorders.session import AmazonSession
from amazonorders.orders import AmazonOrders

amazon_session = AmazonSession("<AMAZON_EMAIL>",
                               "<AMAZON_PASSWORD>")
amazon_session.login()

amazon_orders = AmazonOrders(amazon_session)
orders = amazon_orders.get_order_history(year=2023)

for order in orders:
    print("{} - {}".format(order.order_number, order.grand_total))
```

## Documentation

For more advanced usage, `amazon-orders`'s official documentation is available at [http://amazon-orders.readthedocs.io](http://amazon-orders.readthedocs.io).

## Contributing

If you would like to get involved, be sure to review the [Contribution Guide](https://github.com/alexdlaird/amazon-orders-python/blob/main/CONTRIBUTING.rst).

Want to contribute financially? If you've found `amazon-orders` useful, [sponsorship](https://github.com/sponsors/alexdlaird) would
also be greatly appreciated!