# 簡単な例
class Model:
    def __init__(self):
        self.data = "Hello, MVP!"

class View:
    def display(self, data):
        print(data)

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_view(self):
        self.view.display(self.model.data)

model = Model()
view = View()
presenter = Presenter(model, view)
presenter.update_view()  # Output: Hello, MVP!

