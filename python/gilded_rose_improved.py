# -*- coding: utf-8 -*-
from gilded_rose import Item
from enum import Enum

# The item types 
class ItemType(Enum):
    normal = 1
    aged_brie = 2
    sulfuras = 3
    backstage_pass = 4
    conjured = 5

# This more efficient version of our Gilded Rose shop can identify the types of items we have in stock
# Having this new system, rather than replacing the old one, allows us to validate that
# it produces the same output as the old one
class GildedRoseImproved(object):

    def __init__(self, items):
        self.items = items
        
        # Initialize dictionary
        # The keys is the item type and the value is the functions for updating that item type
        self.item_update_dict = {}
        self.item_update_dict[ItemType.normal] = self.update_normal
        self.item_update_dict[ItemType.aged_brie] = self.update_aged_brie
        self.item_update_dict[ItemType.sulfuras] = self.update_sulfuras
        self.item_update_dict[ItemType.backstage_pass] = self.update_backstage_pass
        self.item_update_dict[ItemType.conjured] = self.update_conjured

    # Updates the shop's inventory quality
    def update_quality(self):
        # For each item, get the item type and invoke the function
        for item in self.items:
            item_type = self.get_item_type(item)
            self.item_update_dict[item_type](item)

    # Fetches the item type for a given item
    def get_item_type(self, item):
        if item.name == "Aged Brie":
            return ItemType.aged_brie
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return ItemType.backstage_pass
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return ItemType.sulfuras
        elif item.name.startswith("Conjured "):
            return ItemType.conjured

        return ItemType.normal

    def update_normal(self, item):
        item.sell_in -= 1

        # Normal items degrade at twice the speed once the sell-in value has expired
        degrade_amt = 2 if item.sell_in < 0 else 1
        item.quality = self.clamp(item.quality - degrade_amt, 0, 50)
    
    def update_aged_brie(self, item):
        item.sell_in -= 1

        # Aged brie always increases in quality - doubly so past the expiration date
        upgrade_amt = 2 if item.sell_in < 0 else 1
        item.quality = self.clamp(item.quality + upgrade_amt, 0, 50)
    
    def update_sulfuras(self, item):
        # Sulfuras doesn't need to be sold and never decreases in quality
        pass
    
    def update_backstage_pass(self, item):
        # If the expiration date is 5 or fewer days away, quality increases by 3
        if item.sell_in <= 5:
            item.quality = self.clamp(item.quality + 3, 0, 50)
        # If expiration is 10 days away, quality increases by 2
        elif item.sell_in <= 10:
            item.quality = self.clamp(item.quality + 2, 0, 50)
        # Otherwise, quality increases by 1
        else:
            item.quality = self.clamp(item.quality + 1, 0, 50)
        
        item.sell_in -= 1

        # However, after the expiration date, backstage passes drop to 0 quality
        if item.sell_in < 0:
            item.quality = 0
    
    def update_conjured(self, item):
        # Conjured items are basically normal items that degrade twice as fast
        # We can simply invoke the normal function twice
        self.update_normal(item)
        
        # Increase the sell-in before updating again so we get the correct value
        # This way the sell-in doesn't go negative before it should, subtracting even more from the quality
        item.sell_in += 1
        
        self.update_normal(item)

    # Helper function to restrict values
    # Primarily used for clamping item quality from 0 to 50 to reduce code duplication
    def clamp(self, val, min, max):
        if val < min:
            return min
        elif val > max:
            return max
        return val