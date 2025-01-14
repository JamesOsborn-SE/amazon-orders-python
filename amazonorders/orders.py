import datetime
import logging
from typing import List, Optional

from amazonorders.conf import DEFAULT_OUTPUT_DIR
from amazonorders.entity.order import Order
from amazonorders.exception import AmazonOrdersError
from amazonorders.session import BASE_URL, AmazonSession

__author__ = "Alex Laird"
__copyright__ = "Copyright 2024, Alex Laird"
__version__ = "1.0.6"

logger = logging.getLogger(__name__)

ORDER_HISTORY_CARD_SELECTOR = "div[class*='js-order-card']"
ORDER_DETAILS_DIV_SELECTOR = "div[id='orderDetails']"
NEXT_PAGE_LINK = "{}/gp/your-account/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter=year-{}{}"
NEXT_PAGE_LINK_SELECTOR = "ul[class*='a-pagination'] li[class*='a-last'] a"


class AmazonOrders:
    """
    Using an authenticated :class:`~amazonorders.session.AmazonSession`, can be used to query Amazon
    for Order details and history.
    """

    def __init__(self,
                 amazon_session: AmazonSession,
                 debug: bool = False,
                 output_dir: str = None) -> None:
        if not output_dir:
            output_dir = DEFAULT_OUTPUT_DIR

        #: The AmazonSession to use for requests.
        self.amazon_session: AmazonSession = amazon_session

        #: Set logger ``DEBUG`` and send output to ``stderr``.
        self.debug: bool = debug
        if self.debug:
            logger.setLevel(logging.DEBUG)
        #: The directory where any output files will be produced, defaults to ``conf.DEFAULT_OUTPUT_DIR``.
        self.output_dir = output_dir

    def get_order_history(self,
                          year: int = datetime.date.today().year,
                          start_index: Optional[int] = None,
                          full_details: bool = False) -> List[Order]:
        """
        Get the Amazon order history for the given year.

        :param year: The year for which to get history.
        :param start_index: The index to start at within the history.
        :param full_details: Will execute an additional request per Order in the retrieved history to fully populate it.
        :return: A list of the requested Orders.
        """
        if not self.amazon_session.is_authenticated:
            raise AmazonOrdersError("Call AmazonSession.login() to authenticate first.")

        orders = []
        next_page = NEXT_PAGE_LINK.format(BASE_URL,
                                                                        year,
                                                                        "&startIndex={}".format(
                                                                            start_index) if start_index else "")
        while next_page:
            self.amazon_session.get(next_page)
            response_parsed = self.amazon_session.last_response_parsed

            for order_tag in response_parsed.select(ORDER_HISTORY_CARD_SELECTOR):
                order = Order(order_tag)

                if full_details:
                    self.amazon_session.get(order.order_details_link)
                    order_details_tag = self.amazon_session.last_response_parsed.select_one(ORDER_DETAILS_DIV_SELECTOR)
                    order = Order(order_details_tag, full_details=True, clone=order)

                orders.append(order)

            next_page = None
            if start_index is None:
                next_page_tag = response_parsed.select_one(NEXT_PAGE_LINK_SELECTOR)
                if next_page_tag:
                    next_page = "{}{}".format(BASE_URL, next_page_tag["href"])
                else:
                    logger.debug("No next page")
            else:
                logger.debug("start_index is given, not paging")

        return orders

    def get_order(self,
                  order_id: str) -> Order:
        """
        Get the Amazon order represented by the ID.

        :param order_id: The Amazon Order ID to lookup.
        :return: The requested Order.
        """
        if not self.amazon_session.is_authenticated:
            raise AmazonOrdersError("Call AmazonSession.login() to authenticate first.")

        self.amazon_session.get("{}/gp/your-account/order-details?orderID={}".format(BASE_URL, order_id))

        order_details_tag = self.amazon_session.last_response_parsed.select_one(ORDER_DETAILS_DIV_SELECTOR)
        order = Order(order_details_tag, full_details=True)

        return order
