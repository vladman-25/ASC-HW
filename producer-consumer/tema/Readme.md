# **Marketplace**

Marketplace by Man Andrei Vlad 336CA, multithreading app in python.

## **1. Marketplace**

Marketplace implements the following methods

### **1.0 Variables**
We will need
- id counter for producer **producer_count**
- id counter for carts **cart_nr**
- array for producers, made of tuples of a Queue and a Lock **producer_array**

### **1.1 register_producer**
This method returns a unique ID for every producer, using a Lock on an Integer. It creates a new Queue and Lock to be stored in **producer_array** as a tuple

### **1.2 publish**
Retrieves the Queue and Lock based on the id provided, synchronizes them to avoid conflicts with consumers, and then adds a product made of a tuple containg product name and a reserved id (-1 initally).

### **1.3 new_cart**
Returns an unique ID for carts, same process as **register_producer**

### **1.4 add_to_cart**
Searches the give product through all the producers. It first gets the Lock and Queue of each producer, in order to synchronize, then sets the item with the cart ID in order to reserve it. The condition to reserve an item is for it be unreserved (id -1), be the item needed (name equality), and it can't be already found in this function. If none is found, we return False.


### **1.5 remove_from_cart**
Searches a product in producers list, that has the same name as the given parameter and is reserved by the cart ID. Sets it as unreserved (id -1) in order to be resold.

### **1.6 place_order**
Searched all products reserved by the cart ID, removes them from the producers Queues, an returns a List made of them.

## **2. Producer**
The Producer Thread
### **2.0 Init**
Initialise the thread and register him for an ID.
### **2.1 Flow**
Cycle through the products that can be made, and produce them in the quantity specified. We then wait some time for simulating the process. After this, it tries to publish the product untill succes.


## **3. Consumer**
### **3.1 Flow**
Cycle through the carts given. Register each cart, and then do the operations asked. For add_product, try untill success. For remove, take it for granted. At the end, place order and use a global Lock to print to stdout. Use a global Lock because any Lock initialised in the Thread is only owned by the Thread and won't be effective.

## **4. Unit Testing**
There are some simple tests to proove the functionality of the Marketplace class. It tests each function and checks if it is right. It doesn't test concurrency.