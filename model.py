from agent import Customer, Store
from mesa import Model, DataCollector
from mesa.space import MultiGrid
from scheduler import RandomActivationByTypeFiltered


class HotellingModel(Model):
    verbose = False  # Print-monitoring
    width = 20,
    height = 20,
    initial_customer_per_cell = 10,
    initial_store = 4,
    distance_sensibity = .1,
    initial_store_price = 10,
    is_customers_stationary = True
    enable_price = True

    def __init__(self, width=20,
                 height=20,
                 initial_customer_per_cell=10,
                 initial_store=5,
                 distance_sensibity=.1,
                 initial_store_price=10,
                 is_customers_stationary=True,
                 enable_price=True
                 ):
        print("Entered")
        super(HotellingModel, self).__init__()
        self.initial_store_price = initial_store_price
        self.distance_sensibity = distance_sensibity
        self.width = width
        self.height = height
        self.customer_per_cell = initial_customer_per_cell
        self.store_nums = initial_store
        self.stationary_cust = is_customers_stationary
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByTypeFiltered(self)
        self.total_cust = 0
        self.customers = []
        self.stores = []
        self.enable_price = enable_price
        for i in range(self.store_nums):
            self.create_store(id=i)

        for i in range(height):
            for j in range(width):
                self.create_customers(i, j)

        model_data_collector = self.get_model_data_collector()
        self.datacollector = DataCollector(
            model_data_collector,
            agent_reporters={"Revenue": lambda x: getattr(x, "revenue", 0)},
        )
        self.datacollector.collect(self)

    def create_store(self, id):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        store = Store(id, (x, y), self.initial_store_price, self)
        self.schedule.add(store)
        self.grid.place_agent(store, (x, y))
        self.stores.append(store)

    def create_customers(self, i, j):
        for _ in range(self.customer_per_cell):
            self.total_cust += 1
            customer = Customer("cust" + str(self.total_cust), (i, j), self.distance_sensibity, model=self)
            self.schedule.add(customer)
            self.grid.place_agent(customer, (i, j))
            self.customers.append(customer)

    def step(self):
        print("Model**********")
        self.schedule.step()
        self.datacollector.collect(self)

    def get_all_customers(self):
        return self.customers

    def get_all_stores(self):
        return self.stores

    def get_rev(self, agent):
        """
        For agent reporters in data collector

        return list of trade partners and None for other agents
        """
        if isinstance(agent, Store):
            # print("agent.revenue", agent.unique_id, agent.revenue)
            return agent.revenue
        else:
            return 0

    def get_trade(self, store_id):
        store = self.get_all_stores()[store_id]
        return store.revenue

    def get_price(self, store_id):
        store = self.get_all_stores()[store_id]
        return store.price

    def get_model_data_collector(self):
        dc = {
            "Store": lambda m: m.schedule.get_type_count(Store),
        }
        stores = self.get_all_stores()

        for store in stores:
            i = store.unique_id
            dc["Store_" + str(store.unique_id)] = [self.get_trade, [i]]
            dc["Store_" + str(store.unique_id) + "_price"] = [self.get_price, [i]]
        return dc
