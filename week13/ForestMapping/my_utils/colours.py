from ai_classes_list import get_attributes_by_key

colours = get_attributes_by_key('rgb_color')


def get_colour(colour):
    if type(colour) == str:
        return colours[colour]
    else:
        raise TypeError(f'Colour must be int. Illegal argument: {colour}')
