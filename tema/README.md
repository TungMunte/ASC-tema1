**_ producer _**

- provide synchronization lock to add product to market, to create id for producer
- we generate id for current producer
- for every product created by current producer, we place it to market
- if success, we will wait for the time that is extracted from the created product
- if failed, we will wait for the republish_wait_time

**_ consumer _**

- provide synchronization lock to add and remove product from cart, to create id for cart
- we create id cart for every cart
- we will operate every operation for the current cart
- after completing all operations for current cart, we will display all remaining products in current cart

**_ market _**

- provide synchronization lock to display available products in cart
- store all available produced products
- map products of a producer with their id
- map current products in carts of consumer with their id
- map current number of products with their producers
