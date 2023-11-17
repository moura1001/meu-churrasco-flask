from src.app import application
from src.logger import mylogger

def print_hi(name):
    mylogger.info(f'Hello, {name}!')

if __name__ == '__main__':
    print_hi('World')
    application.run(debug=False)
