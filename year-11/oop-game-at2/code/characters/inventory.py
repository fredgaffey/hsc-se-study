"""
    this file contains constants the related conastants for the invotry items and their effects
"""
import time
from core.game_object import GameObject

# import string


# class potions(gameobject):

class Potions():
    """
    this is the parent class to make the potions 
    
    the potion stores duration, potion start time, as well as buff multipliers (1.0 is no buff)
    these buffs can be any float and change the effect of pickups/damage/etc.
    """
    cost = 0
    name = None
    quantity  = None
    start_time = None
    duration = None
    key = ""
    gBuf = None
    dBuf = None
    rBuf = None
    sBuf = None

    

    def __init__(self,cost,name,duration,key="",rBuf=1,sBuf=1,dBuf=1,gBuf=1):
        self.cost = cost
        self.name = name
        self.start_time = None
        self.sBuf = sBuf
        self.dBuf = dBuf
        self.rBuf = rBuf
        self.gBuf = gBuf
        self.duration = duration
        self.key = str(key)
    
    @property
    def display_name(self):
        """Get user-friendly display name for the potion."""
        name_mapping = {
            "resistance_potion": "Resistance Potion",
            "speed_potion": "Speed Potion", 
            "gold_potion": "Gold Potion",
            "damage_potion": "Damage Potion"
        }
        return name_mapping.get(self.name, self.name.replace("_", " ").title())
        


class Inventory_manager():
    """this class manages the item in a inventory it is applicable fro both the player and the npc
    """
    num_of_orc_drops = 0

    def __init__(self):
        self.active_potions = []
        self.inventory = []
        self.item_last_used = time.time()
        self.item_last_added = time.time()
        self.enable_buy = False
        self.num_of_orc_drops = 0

    def activate(self,pot_name):
        for pot in self.inventory:
            if pot_name == pot:
                pot.start_time = time.time() 
                self.item_last_used = time.time()
                self.active_potions.append(pot)
                self.inventory.remove(pot)
                print("activated",pot_name)
                break
        
    def add_to_inventory_with_time_safe(self,pot):
        self.inventory.append(pot)
        self.item_last_added = time.time() 
    def add_item(self,item):
        print(item,"added to invoterry")
        self.inventory.append(item)
        
    
            
    def get_active_potion_and_buf(self):
        """
        this functon will return a dict of the types of potions and there multipliers 
        """
        buffs = {
        "gBuf":1,
        "rBuf":1,
        "dBuf":1,
        "sBuf":1}

        for pot in self.active_potions[:]:  # Use slice copy to avoid modification during iteration
            if pot.start_time + pot.duration < time.time():
                # Potion has expired, remove it
                self.active_potions.remove(pot)
            else:
                # Potion is still active, apply its buffs
                buffs['gBuf'] *= pot.gBuf
                buffs['rBuf'] *= pot.rBuf
                buffs['dBuf'] *= pot.dBuf
                buffs['sBuf'] *= pot.sBuf

        buffs['sBuf'] = min( buffs['sBuf'],6)         
        return buffs
    def get_amount_orc_drop(self):
        return self.num_of_orc_drops
    
    def reset_inventory(self):
        self.inventory = []
        return None
    
    def display_contents_count(self):
        """this will make the dict to be displayed for the user

        Returns:
            dict: invotory to be desplayd"""
            
        temp = {"orc drop":self.num_of_orc_drops}
        for i in self.inventory:
            # print("one loop")
            try:
                if temp[i.name]:
                    temp[i.name] += 1
            except KeyError:
                temp[i.name] = 1
        return temp