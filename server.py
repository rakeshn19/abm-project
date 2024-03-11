import mesa

from model import HotellingModel
from agent import Store

width = 10
height = 10
model_params = {
    "height": height,
    "width": width,
    "initial_customer_per_cell": mesa.visualization.Slider(
        "Customer Per Cell", 4, 2, 10, description="Initial Number of Customer per cell"
    ),
    "initial_store": mesa.visualization.Slider(
        "Store Numbers",
        4,
        2,
        10,
        description="Number of stores",
    ),
    "initial_store_price": mesa.visualization.Slider(
        "Store Price",
        10,
        5,
        100,
        description="Store item selling price",
    ),
    "distance_sensibity": 1,
    "is_customers_stationary": True,
    "enable_price": mesa.visualization.Checkbox("Price Enabled", True),
}

COLORS = {"Revenue": "#880000"}

COLORS_AGENTS = ['#37AB65', '#3DF735', '#AD6D70', '#EC2504', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7',
                 '#145JKH']
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
            "text": agent.unique_id,
            "Color": COLORS_AGENTS[agent.unique_id],
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
    t_chart = mesa.visualization.ChartModule(
        [{"Label": label, "Color": color} for (label, color) in colors.items()]
    )
    return t_chart


charts = [canvas_element]
STORE_COLORS = []
tree_chart_map = {}
tree_chart_price_map = {}

for i in range(10):
    tree_chart_map["Store_" + str(i)] = COLORS_AGENTS[i]
    tree_chart_price_map["Store_" + str(i) + "_price"] = COLORS_AGENTS[i]
charts.append(get_tree_charts(tree_chart_map))
charts.append(get_tree_charts(tree_chart_price_map))

agent_bar = mesa.visualization.BarChartModule(
    [{"Label": "Revenue", "Color": MID_COLOR}],
    scope="agent",
    sorting="ascending",
    sort_by="Revenue",
)

server = mesa.visualization.ModularServer(
    HotellingModel, charts, "Hotelling", model_params
)
