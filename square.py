from ship import *
import os


class Square():

    def __init__(self, ship_instance=None):

        self.associated_class_obj = ship_instance
        self.single_square_hit_count = 0

    def was_hit(self):

        if isinstance(self.associated_class_obj, Ship) and self.single_square_hit_count == 0:
            self.associated_class_obj.decrement_hp()
            self.single_square_hit_count = 1
            if self.associated_class_obj.hit_points == 0:
                respond_message = "hit! {} was sunk!".format(self.associated_class_obj.__class__.__name__)
            else:
                respond_message = "hit!"

        elif self.single_square_hit_count == 0:
            self.single_square_hit_count = 1
            respond_message = "miss!"
        else:
            respond_message = "you've already been here."

        return respond_message

    def __str__(self):
        if not self.associated_class_obj:
            if self.single_square_hit_count == 0:
                return " "
            else:
                return '.'
        elif self.single_square_hit_count > 0:
            return "X"
        else:
            return " "
