"""
Coordinates the Model instance with the View.
There is one Controller per program instance.

"""
from MVC.Model import Model
from MVC.View import View


class Controller:
    """Coordinates the Model instance with user interaction via View.

    There should be one instance of the Controller class per program instance.
    """

    def __init__(self):
        self.model = Model()
        self.view = View()


