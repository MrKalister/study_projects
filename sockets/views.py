from os import path


def index():
    current_directory = path.join(
        path.dirname(path.abspath(__file__)), 'temp', 'index.html')
    with open(current_directory) as t:
        return t.read()


def blog():
    current_directory = path.join(
        path.dirname(path.abspath(__file__)), 'temp', 'blog.html')
    with open(current_directory) as t:
        return t.read()
