# 簡単な例
# 簡単な例
class Model:
    def __init__(self):
        self.data = "Hello, MVVM!"

class ViewModel:
    def __init__(self, model):
        self.model = model

    def get_data(self):
        return self.model.data

class View:
    def display(self, data):
        print(data)

model = Model()
view_model = ViewModel(model)
view = View()
view.display(view_model.get_data())  # Output: Hello, MVVM!


