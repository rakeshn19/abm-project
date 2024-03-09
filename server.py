import mesa

from model import HotellingModel
from agent import Store


width=10
height=10
agents_count = 4
COLORS = {"Revenue": "#880000"}
#STORE_COLORS["Store"+i]= "#880000"
# "Revenue": "#880000", "cust": "#000000", "Store": "#00AA00"
MID_COLOR = "#1f77b4"
def Agent_portrayal(agent):
    if agent is None:
        return
    if isinstance(agent, Store):
        return {
            "Shape": "circle",
            "Filled": "true",
            "r": 1,
            "Layer": 0,
            "Color": "#FF0A01",
        }


canvas_element = mesa.visualization.CanvasGrid(
    Agent_portrayal, width, height, 500, 500
)
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

def get_tree_charts(colors):
    tree_chart = mesa.visualization.ChartModule(
            [{"Label": label, "Color": color} for (label, color) in colors.items()]
    )
    return tree_chart

charts = [canvas_element]
STORE_COLORS =[] #{"Store0": "#880000"}
for i in range(agents_count):
    color = {"Store"+str(i): "#880000"}
    charts.append(get_tree_charts(color))




agent_bar = mesa.visualization.BarChartModule(
    [{"Label": "Revenue", "Color": MID_COLOR}],
    scope="agent",
    sorting="ascending",
    sort_by="Revenue",

)


model_params = {
    "height": height,
    "width": width,
    "initial_customer_per_cell": 3,
    "initial_store": agents_count,
    "distance_sensibity": .2,
    "initial_store_price": 10,
    "is_customers_stationary": True
}

'''
  def __init__(self, width=20,
                 height=20,
                 initial_customer_per_cell=10,
                 initial_store=5,
                 distance_sensibity = .1,
                 initial_store_price = 10,
                 is_customers_stationary=True):
        super(HotellingModel, self).__init__()
'''



#Hotelier, [canvas_element, tree_chart, pie_chart], "test", model_params
server = mesa.visualization.ModularServer(
   HotellingModel, charts,"test", model_params
)
'''server = mesa.visualization.ModularServer(
   HotellingModel, [canvas_element, tree_chart, agent_bar],"test", model_params
)'''

