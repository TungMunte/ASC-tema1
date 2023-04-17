"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import time
from logging.handlers import RotatingFileHandler
from threading import Lock

logging.Formatter.converter = time.gmtime
logging.basicConfig(
    handlers=[RotatingFileHandler(filename='marketplace.log', maxBytes=213000, backupCount=10)],
    level=logging.INFO,
    format="%(asctime)s : %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S')

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.lock_sizes = Lock()  # used to modify a producer's queue size
        self.lock_num_carts = Lock()  # used to modify the number of carts
        self.lock_producer_id = Lock()  # used to register a producer atomically
        self.lock_print = Lock()  # used in order not to interleave the prints

        self.queue_size_per_producer = queue_size_per_producer
        self.num_carts = 0

        self.prod_q_sizes = {}  # a producer's number of items in the queue
        self.products = []  # the queue containing all available items
        self.carts = {}  # a dictionary of lists each representing a cart
        self.producers = {}  # a dictionary mapping products to their producers

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock_producer_id:
            logging.info('register_producer')
            prod_id = self.prod_q_sizes.__len__()
            self.prod_q_sizes[prod_id] = 0
        return prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        logging.info('publish')
        id_producer = int(producer_id)
        if self.prod_q_sizes[id_producer] >= self.queue_size_per_producer:
            return False
        self.producers[product] = id_producer
        self.prod_q_sizes[id_producer] += 1
        self.products.append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_num_carts:
            logging.info('new_cart')
            self.num_carts += 1
            self.carts[self.num_carts] = []
            cart_id = self.num_carts
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.lock_sizes:
            logging.info('add_to_cart')
            if product not in self.products:
                return False
            self.carts[cart_id].append(product)
            self.prod_q_sizes[self.producers[product]] -= 1
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.lock_sizes:
            logging.info('remove_from_cart')
            if product not in self.carts[cart_id]:
                return False
            self.carts[cart_id].remove(product)
            self.prod_q_sizes[self.producers[product]] += 1
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logging.info('place_order')
        return self.carts[cart_id]
