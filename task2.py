# [10,50,20,30,70] these are daily prices. You can buy or sell at either price.

def find_largest_loss(prices):
    if len(prices) < 2:
        return 0
    largest_loss = 0
    max_price_found = prices[0]
    for price in prices:
        if price > max_price_found:
            max_price_found = price
        else:
            loss_selling_at_this_price = max_price_found - price
            if loss_selling_at_this_price > largest_loss:
                largest_loss = loss_selling_at_this_price
    return largest_loss


from unittest import TestCase

class TestLargestLoss(TestCase):
    def test_empty_prices(self):
        prices = []
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 0)

    def test_normal_array_of_prices(self):
        prices = [10, 50, 20, 30, 70]
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 30)

    def test_one(self):
        prices = [50]
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 0)

    def test_some_negative_prices(self):
        # I guess you buy for 10 and then you have to pay them 25 to take it?
        prices = [10, -25, 5, 20]
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 35)

    def test_all_negative_prices(self):
        prices = [-10, -25, -5, -20, -50, -100, -5]
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 95)

    def test_prices_equal(self):
        prices = [20, 20, 20, 20]
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 0)

    def test_big_array(self):
        from random import randint
        prices = [randint(10, 100) for x in range(1000000)]
        prices[4000] = 200
        prices[500000] = 5
        largest_loss = find_largest_loss(prices)
        self.assertEqual(largest_loss, 195)




