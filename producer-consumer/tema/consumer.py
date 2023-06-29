"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, Lock
import time

printer = Lock()

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
        Thread.__init__(self)
        self.kwargs = kwargs
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cartid = self.marketplace.new_cart()
            for action in cart:
                if action['type'] == 'add':
                    qt = int(action['quantity'])
                    for i in range(qt):
                        while not self.marketplace.add_to_cart(cartid,action['product']):
                            time.sleep(self.retry_wait_time)
                if action['type'] == 'remove':
                    qt = int(action['quantity'])
                    for i in range(qt):
                        self.marketplace.remove_from_cart(cartid,action['product'])
            order = self.marketplace.place_order(cartid)
            printer.acquire()
            for item in order:
                print(self.kwargs['name'] + " bought " + str(item))
            printer.release()
