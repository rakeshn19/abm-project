import random

import mesa
from random_walk import RandomWalker
import math


class Customer(mesa.Agent):

    def __init__(self, ID, pos, distance_sensibity, model):
        self.distance_sensibity = distance_sensibity
        self.model = model
        self.unique_id = ID
        self.store_info = {}
        self.pos = pos
        self.choosen_store = None
        self.current_price = None

    def step(self) -> None:
        #print("Customer")
        self.choose_store()

    def will_choose_new_store(self, pos, price):
        new_price = self.calculate_price(pos, price)
        return (self.current_price is None or new_price < self.current_price), new_price

    def will_choose_new_price(self, location, price):
        new_price = self.calculate_price(location, price)#price + self.calculate_distance_price_factor(location)
        return self.current_price is None or new_price < self.current_price, new_price

    def calculate_price(self, loc, price):
        new_price = price + self.calculate_distance_price_factor(loc)
        return new_price

    def choose_store(self):
        stores = self.model.get_all_stores()
        for store in stores:
            is_min, new_price = self.will_choose_new_store(store.pos, store.price)
            if is_min:
                self.choosen_store = store
                self.current_price = new_price
        self.choosen_store.transact(self)

    def calculate_distance_price_factor(self, store_pos):
        x1, y1 = store_pos
        x2, y2 = self.pos
        # Calculate the distance
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        #print(distance)
        return distance #*  self.distance_sensibity


class Store(RandomWalker):
    def __init__(self, ID, pos, price, model):
        super(Store, self).__init__(id, pos, model)
        self.model = model
        self.unique_id = ID
        self.customers = {}
        self.price = price
        self.pos = pos
        self.profit = 0
        self.revenue = 0

    def step(self) -> None:
        if self.profit != 0:
            self.revenue = self.profit
        profit_with_move, new_loc = self.calculate_profit_after_move()
        if profit_with_move > self.profit:
            print("Agent ", self.unique_id, "moving")
            self.model.grid.move_agent(self, new_loc)
            self.pos = new_loc
        new_profit, new_price = self.calculate_profit_after_price_change()
        if new_profit > self.profit:
            print("Agent ", self.unique_id , " is changing price from",self.price, "to new price", new_price)
            self.price = new_price
        self.reset()

    def transact(self, customer: Customer):
        #print("cust", customer.unique_id, "store",self.unique_id, " are transacting", self.profit)
        self.profit += self.price

    def get_location(self):
        return self.pos

    def get_price(self):
        return self.price

    def calculate_profit_after_move(self):
        new_loc = self.next_possible_move()
        total_profit_after_move = self.calculate_profit_by_location(new_loc)
        return total_profit_after_move, new_loc

    def calculate_profit_after_price_change(self):
        price_update = [1, -1]
        new_price = self.price + random.choice(price_update)
        if new_price < 1:
            return -1, 1
        new_profit = self.calculate_profit_by_price(new_price)
        return new_profit, new_price

    def calculate_profit_by_location(self, store_pos):
        customers = self.model.get_all_customers()
        total_profit = 0
        for customer in customers:
            is_min, _ = customer.will_choose_new_store(store_pos, self.price)
            if is_min:
                total_profit += self.price
        return total_profit

    def calculate_profit_by_price(self, new_price):
        customers = self.model.get_all_customers()
        total_profit = 0
        for customer in customers:
            is_min, _ = customer.will_choose_new_price(self.pos, new_price)
            if is_min:
                total_profit += new_price
        return total_profit

    def reset(self):
        self.profit = 0
