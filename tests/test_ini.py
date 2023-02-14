import json
import os

print(os.path.dirname(__file__))

with open(f'{os.path.dirname(__file__)}/../gpio.json', 'r') as j:
    gpio_loc = json.loads(j.read())

print(gpio_loc)

print(type(gpio_loc['active']))
