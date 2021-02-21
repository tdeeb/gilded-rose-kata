# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item
from gilded_rose_improved import GildedRoseImproved

# Unit tests for our improved version of Gilded Rose
# These are the same test cases as the ones for the original Gilded Rose, with the exception of Conjured items
# This allows us to verify the output is the same
class GildedRoseImprovedTest(unittest.TestCase):
    def test_agedbrie_expired(self):
        items = [Item("Aged Brie", 0, 0)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 2)
    
    def test_agedbrie_qualityincrease(self):
        items = [Item("Aged Brie", 5, 3)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 4)
    
    def test_agedbrie_maxquality(self):    
        items = [Item("Aged Brie", 3, 48)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 2)
        self.assertEqual(items[0].quality, 49)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 50)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 50)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 50)

    def test_sulfuras(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 8, 5)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        # Sulfuras never degrades
        self.assertEqual(items[0].quality, 5)
        self.assertEqual(items[0].sell_in, 8)
    
    def test_normal(self):
        items = [Item("MyItem1", 2, 8)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 7)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 6)
        gilded_rose.update_quality()
        # Degrades twice as fast past sell-in
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 4)

    def test_normal_qualitygtezero(self):
        items = [Item("MyItem2", 7, 1)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 6)
        self.assertEqual(items[0].quality, 0)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 5)
        self.assertEqual(items[0].quality, 0)

    def test_backstage_pass_quality_gte11(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 11, 17)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 10)
        self.assertEqual(items[0].quality, 18)
    
    def test_backstage_pass_quality_gte6(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 6, 15)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 5)
        self.assertEqual(items[0].quality, 17)

    def test_backstage_pass_quality_gte1(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 1, 19)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 22)
    
    def test_backstage_pass_quality_sellinzero(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 50)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 0)

    def test_conjured(self):
        items = [Item("Conjured MyItem1", 2, 8)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 6)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 4)
        gilded_rose.update_quality()
        # Degrades twice as fast past sell-in
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 0)

    def test_conjured_qualitygtezero(self):
        items = [Item("Conjured MyItem2", 7, 1)]
        gilded_rose = GildedRoseImproved(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 6)
        self.assertEqual(items[0].quality, 0)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 5)
        self.assertEqual(items[0].quality, 0)
    
if __name__ == '__main__':
    unittest.main()
