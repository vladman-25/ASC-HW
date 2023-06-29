"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.
        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self,daemon=True)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.prod_index = 0
        self.id = marketplace.register_producer()
        self.kwargs = kwargs

    def run(self):
        while(True):

            product = self.products[self.prod_index]
            qty = product[1]
            name = product[0]
            time.sleep(product[2])
            for i in range(qty):
                while(not self.marketplace.publish(self.id,name)):
                    time.sleep(self.republish_wait_time)

            self.prod_index += 1
            self.prod_index = self.prod_index % len(self.products)
