classes = {
    # 'forest_fire': [
    #     {'name': 'alive_trees', 'title': 'Medium Risk', 'hex_color': '#FFD800', 'rgb_color': (255, 216, 0)},
    #     {'name': 'dead_trees', 'title': 'High Risk', 'hex_color': '#E74C3C', 'rgb_color': (231, 76, 60)}
    # ],
    # 'rails': [
    #     {'name': '0', 'title': '0', 'hex_color': '#fcb924', 'rgb_color': (252,185,36)},
    #     {'name': 'missing_tie', 'title': 'Missing Tie', 'hex_color': '#6eb440', 'rgb_color': (110,180,64)},
    #     {'name': '2', 'title': '2', 'hex_color': '#a8d59e', 'rgb_color': (168,213,158)},
    #     {'name': 'water_pooling', 'title': 'Water Pooling', 'hex_color': '#0f6bb3', 'rgb_color': (15,107,179)},
    #     {'name': '4', 'title': '4', 'hex_color': '#891f05', 'rgb_color': (137,31,5)}
    # ],
    # 'extras': [
    #     {'name': 'green', 'title': 'green', 'hex_color': '#00FF00', 'rgb_color': (70, 220, 70)},
    #     {'name': 'yellow', 'title': 'yellow', 'hex_color': '#FFFF00', 'rgb_color': (255, 216, 0)},
    #     {'name': 'red', 'title': 'yellow', 'hex_color': '#FF0000', 'rgb_color': (231, 76, 60)}
    # ],
    'risks': [
        {'name': 'Alive Tree', 'title': 'green', 'hex_color': '#00FF00', 'rgb_color': (70, 230, 70)},
        {'name': 'Beetle-Fire Tree', 'title': 'red', 'hex_color': '#FF0000', 'rgb_color': (255, 5, 5)},
        {'name': 'Dead Tree', 'title': 'yellow', 'hex_color': '#FFFF00', 'rgb_color': (255, 250, 0)},
        {'name': 'Debris', 'title': 'brown', 'hex_color': '#964B00', 'rgb_color': (150, 75, 0)},
        {'name': 'Background', 'title': 'blue', 'hex_color': '#0000FF', 'rgb_color': (30, 30, 255)}
    ]
}

def get_attributes_by_key(key):
    '''
    Available keys: 'title', 'hex_color', 'rgb_color'
    '''
    result = dict()
    for k in classes:
        for cls in classes[k]:
            result[cls['name']] = cls[key]
    return result

def get_keys():
    result = dict()
    for k in classes:
        result[k] = [cls['name'] for cls in classes[k]]
    return result

