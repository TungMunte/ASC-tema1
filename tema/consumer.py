"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        super().__init__(**kwargs)

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for op in cart:
                quantity = 0
                while quantity < op['quantity']:
                    if op['type'] == 'add':
                        res = self.marketplace.add_to_cart(cart_id, op['product'])
                        if not res:
                            time.sleep(self.retry_wait_time)
                        else:
                            quantity += 1
                    elif op['type'] == 'remove':
                        res = self.marketplace.remove_from_cart(cart_id, op['product'])
                        if not res:
                            time.sleep(self.retry_wait_time)
                        else:
                            quantity += 1
            products_bought = self.marketplace.place_order(cart_id)
            with self.marketplace.lock_print:
                for product in products_bought:
                    print(self.name, 'bought', product)
