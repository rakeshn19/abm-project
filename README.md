# HOTELLING, PRICE COMPETITION, AGENT-BASED MODELING

## Summary

In a pioneering paper Hotelling (1929) presented a model of two firms competing to sell a homo- geneous product to customers uniformly distributed along a line. Though the Hotelling model has been extended in many ways1, no one has produced a general model of spatial competition between more than two firms in a two-dimensional space, with both price and location as choice variables. The problem is important because competition in the real world seldom occurs between two firms on a one-dimensional space. Most products have multiple attributes and multiple firms supplying them.
## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``run.py``: Launches a model visualization server.
* ``model.py``: Contains the agent class, and the overall model class.
* ``server.py``: Defines classes for visualizing the model (network layout) in the browser via Mesa's modular server, and instantiates a visualization server.

