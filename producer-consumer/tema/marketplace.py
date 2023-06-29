"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
from queue import Queue
import logging
from logging.handlers import RotatingFileHandler
import unittest
logging.basicConfig(filename='tema/marketplace.log',
                    encoding='utf-8', 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s')


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
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_array = []
        self.producer_count = 0
        self.queue_id_lock = Lock()
        self.cart_nr = 0
        self.carts_id_lock = Lock()
        self.carts = []
        logging.info('Initiated Marketplace')

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.queue_id_lock.acquire()

        aux = self.producer_count
        prod_queue = Queue(maxsize=self.queue_size_per_producer)
        prod_lock = Lock()

        self.producer_array.append((prod_queue,prod_lock))
        logging.info('Producer %d registered',self.producer_count)
        self.producer_count += 1
        self.queue_id_lock.release()
        return aux

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        self.
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        (q, l) = self.producer_array[producer_id]
        action = False
        l.acquire()
        (q, l) = self.producer_array[producer_id]
        if q.qsize() < self.queue_size_per_producer:
            q.put((product,-1))
            action = True
    
        answear = "SUCCES" if action else "FAILURE"

        logging.info('Producer %s published %s with %s',producer_id,product,answear)
        l.release()

        return action
            
    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_id_lock.acquire()
        cart_id = self.cart_nr
        self.cart_nr += 1

        self.carts_id_lock.release()

        logging.info('Cart %d created',cart_id)
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
        found = False
        for i in range(0,len(self.producer_array)):
            (q, l) = self.producer_array[i]
            l.acquire()
            (q, l) = self.producer_array[i]
            newq = Queue()
            while not q.empty():
                (item, state) = q.get()
                if (item == product) and (state == -1) and (found == False):
                    newq.put((item ,cart_id))
                    found = True
                else:
                    newq.put((item,state))

            self.producer_array[i] = (newq, l)
            l.release()
            if found:
                break
        
        answear = "SUCCES" if found else "FAILURE"
        logging.info('Cart %d add product %s with %s',cart_id,product,answear)
        return found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        found = False
        for i in range(0,len(self.producer_array)):
            (q, l) = self.producer_array[i]
            l.acquire()
            (q, l) = self.producer_array[i]
            newq = Queue()

            while not q.empty():
                (item, state) = q.get()
                if (item == product) and (state == cart_id) and (found == False):
                    newq.put((item ,-1))
                    found = True
                else:
                    newq.put((item,state))
            self.producer_array[i] = (newq, l)

            l.release()
            if found:
                break
        logging.info('Cart %d remove product %s',cart_id,product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        order = []

        for i in range(0,len(self.producer_array)):
            (q, l) = self.producer_array[i]
            l.acquire()
            (q, l) = self.producer_array[i]
            newq = Queue()

            while not q.empty():
                (item, state) = q.get()
                if state == cart_id:
                    order.append(item)
                else:
                    newq.put((item,state))
            self.producer_array[i] = (newq, l)

            l.release()
        logging.info('Cart %d place order',cart_id)
        return order
    
class TestMarketplace(unittest.TestCase):
        
    def setUp(self):
        self.marketplace = Marketplace(5)
        self.product0 = "Coffee(name='Brasil', price=7, acidity=5.09, roast_level='MEDIUM')"
        self.product1 = "Coffee(name='Ethiopia', price=10, acidity=5.09, roast_level='MEDIUM')"
        self.product2 = "Coffee(name='Indonezia', price=1, acidity=5.05, roast_level='MEDIUM')"
        self.product3 = "Tea(name='Cactus fig', price=3, type='Green')"

    def test_register_producer(self):
        self.assertEqual(self.marketplace.register_producer(),0,'prod0 worng')
        self.assertEqual(self.marketplace.register_producer(),1,'prod1 worng')
        self.assertEqual(self.marketplace.register_producer(),2,'prod2 worng')

    def test_publish(self):
        self.test_register_producer()
        self.assertEqual(self.marketplace.publish(0,self.product0),True,'prod0 worng')
        self.assertEqual(self.marketplace.publish(0,self.product0),True,'prod0 worng')
        self.assertEqual(self.marketplace.publish(0,self.product0),True,'prod0 worng')
        self.assertEqual(self.marketplace.publish(0,self.product0),True,'prod0 worng')
        self.assertEqual(self.marketplace.publish(0,self.product0),True,'prod0 worng')
        self.assertEqual(self.marketplace.publish(0,self.product0),False,'prod0 worng')

    def test_new_cart(self):
        self.test_publish()
        self.assertEqual(self.marketplace.new_cart(),0,'cart wrong')
        self.assertEqual(self.marketplace.new_cart(),1,'cart wrong')

    def test_add_to_cart(self):
        self.test_new_cart()
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), False, 'cart wrong')

    def test_remove_from_cart(self):
        self.test_add_to_cart()
        self.marketplace.remove_from_cart(0,self.product0)
        self.assertEqual(self.marketplace.add_to_cart(0,self.product0), True, 'cart wrong')

    def test_place_order(self):
        self.test_remove_from_cart()
        self.assertEqual(self.marketplace.place_order(0),[self.product0,self.product0,self.product0,self.product0,self.product0], 'order wrong')

