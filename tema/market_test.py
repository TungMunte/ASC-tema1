import unittest

from marketplace import Marketplace
from product import Tea, Coffee


class TestMartketplace(unittest.TestCase):

    def setUp(self) -> None:
        self.product01 = Coffee(name="Indonezia", acidity="5.05", roast_level="MEDIUM", price=1)
        self.product02 = Tea(name="Linden", type="Herbal", price=9)
        self.marketplace = Marketplace(20)

    def tearDown(self) -> None:
        print('tear down')

    def test_register_producer(self):
        producer_id_01 = self.marketplace.register_producer()
        producer_id_02 = self.marketplace.register_producer()
        producer_id_03 = self.marketplace.register_producer()
        producer_id_04 = self.marketplace.register_producer()
        producer_id_05 = self.marketplace.register_producer()

        self.assertEqual(producer_id_01, 0)
        self.assertEqual(producer_id_02, 1)
        self.assertEqual(producer_id_03, 2)
        self.assertEqual(producer_id_04, 3)
        self.assertEqual(producer_id_05, 4)

    def test_publish(self):
        producer_id_01 = self.marketplace.register_producer()
        producer_id_02 = self.marketplace.register_producer()
        producer_id_03 = self.marketplace.register_producer()
        producer_id_04 = self.marketplace.register_producer()
        producer_id_05 = self.marketplace.register_producer()

        self.assertEqual(self.marketplace.publish(producer_id_01, self.product01), True)
        self.assertEqual(self.marketplace.publish(producer_id_02, self.product01), True)
        self.assertEqual(self.marketplace.publish(producer_id_03, self.product01), True)
        self.assertEqual(self.marketplace.publish(producer_id_04, self.product01), True)
        self.assertEqual(self.marketplace.publish(producer_id_05, self.product01), True)
        self.assertEqual(self.marketplace.products.__len__(), 5)

    def test_new_cart(self):
        self.assertEqual(self.marketplace.new_cart(), 1)
        self.assertEqual(self.marketplace.new_cart(), 2)
        self.assertEqual(self.marketplace.new_cart(), 3)
        self.assertEqual(self.marketplace.new_cart(), 4)
        self.assertEqual(self.marketplace.new_cart(), 5)

    def test_add_to_cart(self):
        card_id_01 = self.marketplace.new_cart()
        card_id_02 = self.marketplace.new_cart()
        card_id_03 = self.marketplace.new_cart()
        card_id_04 = self.marketplace.new_cart()
        card_id_05 = self.marketplace.new_cart()

        self.assertEqual(self.marketplace.add_to_cart(card_id_01, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_02, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_03, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_04, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_05, self.product01), False)

        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, self.product01)
        self.assertEqual(self.marketplace.add_to_cart(card_id_01, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_02, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_03, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_04, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_05, self.product01), True)

        self.assertEqual(self.marketplace.carts.__len__(), 5)

    def test_remove_from_cart(self):
        card_id_01 = self.marketplace.new_cart()
        card_id_02 = self.marketplace.new_cart()
        card_id_03 = self.marketplace.new_cart()
        card_id_04 = self.marketplace.new_cart()
        card_id_05 = self.marketplace.new_cart()

        self.assertEqual(self.marketplace.add_to_cart(card_id_01, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_02, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_03, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_04, self.product01), False)
        self.assertEqual(self.marketplace.add_to_cart(card_id_05, self.product01), False)

        producer_id_01 = self.marketplace.register_producer()
        producer_id_02 = self.marketplace.register_producer()
        producer_id_03 = self.marketplace.register_producer()
        producer_id_04 = self.marketplace.register_producer()
        producer_id_05 = self.marketplace.register_producer()

        self.marketplace.publish(producer_id_01, self.product01)
        self.marketplace.publish(producer_id_01, self.product02)

        self.marketplace.publish(producer_id_02, self.product01)
        self.marketplace.publish(producer_id_02, self.product02)

        self.marketplace.publish(producer_id_03, self.product01)
        self.marketplace.publish(producer_id_03, self.product02)

        self.marketplace.publish(producer_id_04, self.product01)
        self.marketplace.publish(producer_id_04, self.product02)

        self.marketplace.publish(producer_id_05, self.product01)
        self.marketplace.publish(producer_id_05, self.product02)

        self.assertEqual(self.marketplace.add_to_cart(card_id_01, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_02, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_03, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_04, self.product01), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_05, self.product01), True)

        self.assertEqual(self.marketplace.add_to_cart(card_id_01, self.product02), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_02, self.product02), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_03, self.product02), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_04, self.product02), True)
        self.assertEqual(self.marketplace.add_to_cart(card_id_05, self.product02), True)

        self.assertEqual(self.marketplace.carts.__len__(), 5)

        self.assertEqual(self.marketplace.remove_from_cart(card_id_01, self.product02), True)
        self.assertEqual(self.marketplace.remove_from_cart(card_id_02, self.product02), True)
        self.assertEqual(self.marketplace.remove_from_cart(card_id_03, self.product02), True)
        self.assertEqual(self.marketplace.remove_from_cart(card_id_04, self.product02), True)
        self.assertEqual(self.marketplace.remove_from_cart(card_id_05, self.product02), True)

        self.assertEqual(self.marketplace.carts.__len__(), 5)

    def test_place_order(self):
        card_id_01 = self.marketplace.new_cart()
        card_id_02 = self.marketplace.new_cart()
        card_id_03 = self.marketplace.new_cart()
        card_id_04 = self.marketplace.new_cart()
        card_id_05 = self.marketplace.new_cart()

        producer_id_01 = self.marketplace.register_producer()
        producer_id_02 = self.marketplace.register_producer()
        producer_id_03 = self.marketplace.register_producer()
        producer_id_04 = self.marketplace.register_producer()
        producer_id_05 = self.marketplace.register_producer()

        self.marketplace.publish(producer_id_01, self.product01)
        self.marketplace.publish(producer_id_02, self.product01)
        self.marketplace.publish(producer_id_03, self.product01)
        self.marketplace.publish(producer_id_04, self.product01)
        self.marketplace.publish(producer_id_05, self.product01)

        self.marketplace.publish(producer_id_01, self.product02)
        self.marketplace.publish(producer_id_02, self.product02)
        self.marketplace.publish(producer_id_03, self.product02)
        self.marketplace.publish(producer_id_04, self.product02)
        self.marketplace.publish(producer_id_05, self.product02)

        self.marketplace.add_to_cart(card_id_01, self.product01)
        self.marketplace.add_to_cart(card_id_02, self.product01)
        self.marketplace.add_to_cart(card_id_03, self.product01)
        self.marketplace.add_to_cart(card_id_04, self.product01)
        self.marketplace.add_to_cart(card_id_05, self.product01)

        self.marketplace.add_to_cart(card_id_01, self.product02)
        self.marketplace.add_to_cart(card_id_02, self.product02)
        self.marketplace.add_to_cart(card_id_03, self.product02)
        self.marketplace.add_to_cart(card_id_04, self.product02)
        self.marketplace.add_to_cart(card_id_05, self.product02)

        self.assertEqual(self.marketplace.place_order(card_id_01).__len__(), 2)
        self.assertEqual(self.marketplace.place_order(card_id_02).__len__(), 2)
        self.assertEqual(self.marketplace.place_order(card_id_03).__len__(), 2)
        self.assertEqual(self.marketplace.place_order(card_id_04).__len__(), 2)
        self.assertEqual(self.marketplace.place_order(card_id_05).__len__(), 2)
