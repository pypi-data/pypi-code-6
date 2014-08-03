from itertools import chain

from kivy.metrics import dp
from kivy.properties import StringProperty, ReferenceListProperty, NumericProperty, ObjectProperty
from kivy.uix.bubble import Bubble
import math

__author__ = 'Eric'
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from collections import namedtuple
from fish_point import FishPoint
from image_size_data import polygon_sort


class DrawingState(object):
    def __init__(self):
        self.lines = []
        self.first_touch = namedtuple('Point', 'x y')
        self.first_touch.x = -1
        self.first_touch.y = -1
        self.is_drawing = False

        self.mode = None
        self.current_subtype = ""
        self.current_type = ""
        self.current_code = ""

        # Used for area
        self.first_point = None
        self.poly_points = None
        self.poly_line = None

        self.fish_points = []


    def get_lines_text(self):
        text = ""
        for line in self.lines:
            if len(line.points) >= 4:
                line_length = ((line.points[0] - line.points[2]) ** 2 + (line.points[1] - line.points[3]) ** 2) ** 0.5
                text += str(line_length) + '\n'

        return text


class FishBubble(Bubble):
    fish_label = StringProperty()
    point_pos_x = NumericProperty()
    point_pos_y = NumericProperty()
    point_pos = ReferenceListProperty(point_pos_x, point_pos_y)
    scaled_font_size = NumericProperty(int(dp(14)))

    def __init__(self, fish_point, paint_widget, **kwargs):
        super(FishBubble, self).__init__(**kwargs)

        self.fish_point = fish_point
        self.fish_label = "[b]{}[/b]\n{}".format(fish_point.index, fish_point.fish_subtype)
        if fish_point.organism_length:
            try:
                length = float(fish_point.organism_length)
                if not math.isnan(length):
                    self.fish_label += "\n{:.2f} cm".format(length)
            except:
                pass
        if fish_point.organism_area:
            try:
                area = float(fish_point.organism_area)
                if not math.isnan(area):
                    self.fish_label += "\n{:.2f} cm[sup]2[/sup]".format(area)
            except:
                pass

        self.point_pos = (fish_point.pos_x, fish_point.pos_y)
        self.action_bubble = None
        self.paint_widget = paint_widget

        self.set_font_size(None, self.paint_widget.font_scale)
        self.paint_widget.bind(font_scale=self.set_font_size)

    def set_font_size(self, instance, value):
        self.scaled_font_size = int(dp(14) * value)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.toggle_action_bubble()
            return True
        else:
            if self.action_bubble:
                self.toggle_action_bubble()
        return super(FishBubble, self).on_touch_down(touch)

    def toggle_action_bubble(self):
        if self.action_bubble:
            self.parent.remove_widget(self.action_bubble)
            self.action_bubble = None
        else:
            self.action_bubble = FishActionBubble(self.fish_point, self)
            self.parent.add_widget(self.action_bubble)


class FishActionBubble(Bubble):
    point_pos_x = NumericProperty()
    point_pos_y = NumericProperty()
    point_pos = ReferenceListProperty(point_pos_x, point_pos_y)

    def __init__(self, fish_point, fish_bubble, **kwargs):
        super(FishActionBubble, self).__init__(**kwargs)

        self.fish_point = fish_point
        self.fish_bubble = fish_bubble
        self.point_pos = (fish_point.pos_x, fish_point.pos_y)

    def do_length(self):
        self.fish_bubble.toggle_action_bubble()
        self.fish_bubble.paint_widget.do_length(self.fish_point)

    def do_area(self):
        self.fish_bubble.toggle_action_bubble()
        self.fish_bubble.paint_widget.do_area(self.fish_point)

    def do_remove(self):
        self.fish_bubble.toggle_action_bubble()
        self.fish_bubble.paint_widget.remove_fish_point(self.fish_point)


class PaintWidget(Widget):
    fish_points = ObjectProperty(None)
    scatter_scale = NumericProperty() # used to keep track of the scale
    font_scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)

        self.drawing_state = DrawingState()

        self._fish_points = []

        self.dot_color = (0, 1, 1, .9)
        self.dot_size = dp(8)

        self.current_point = None
        self.telem_entry = None

        self.font_scale_enabled = True

        self.bind(scatter_scale=self.set_font_scale)

    def clear(self):
        self.clear_widgets()
        self.canvas.clear()

    def refresh(self):
        self.clear()

        self._fish_points = self.fish_points
        for fish_point in self._fish_points:
            self.draw_fish_point(fish_point)
            if fish_point.line:
                self.draw_line(fish_point.line)
            if fish_point.polygon:
                self.draw_polygon(fish_point.polygon)

    def set_font_scale(self, instance, value):
        # we want to grow the font when we zoom out so everything remains the same size
        # it looks like crap if we decrease the font size, so don't go below 0.
        if not self.font_scale_enabled or (value > 1):
            self.font_scale = 1
        else:
            self.font_scale = 1. / value

    def get_next_index(self):
        max_num = 0
        # Get the highest number already used.
        for point in self.fish_points:
            try:
                if self.drawing_state.current_code in point['index']:
                    this_num = int(point['index'][2:])
                    if this_num > max_num:
                        max_num = this_num
            except:
                pass

        new_num = max_num + 1

        return "{}{}".format(self.drawing_state.current_code, new_num)

    def draw_fish_point(self, point):
        x = point.pos_x
        y = point.pos_y

        # We are counting, so draw a dot.
        with self.canvas:
            d = self.dot_size
            Color(*self.dot_color)
            Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))

        # Now, draw the bubble.
        bubble = FishBubble(point, self)
        self.add_widget(bubble)

    def draw_line(self, line):
        with self.canvas:
            Color(0, 1, 0, 1)
            d = dp(5)
            for point in line:
                Ellipse(pos=(point[0] - d / 2, point[1] - d / 2), size=(d, d))

            Line(points=list(chain.from_iterable(line)))

    def draw_polygon(self, polygon):
        with self.canvas:
            Color(0, 1, 0, 1)

            full_points = polygon + [polygon[0]]
            Line(points=list(chain.from_iterable(full_points)))

    def remove_fish_point(self, fish_point):
        self._fish_points.remove(fish_point)
        self.fish_points = self._fish_points
        self.refresh()

    def do_length(self, fish_point):
        self.drawing_state.mode = 'length'
        self.current_point = fish_point

    def do_area(self, fish_point):
        self.drawing_state.mode = 'area'
        self.current_point = fish_point


    def start_count(self):
        self.drawing_state.mode = 'count'

    def stop_count(self):
        self.drawing_state.mode = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.drawing_state.mode is 'count':
                # Add this fish to the list
                this_point = FishPoint(pos_x=touch.x, pos_y=touch.y, index=self.get_next_index(),
                                       fish_type=self.drawing_state.current_type,
                                       fish_subtype=self.drawing_state.current_subtype)

                self._fish_points.append(this_point)
                self.fish_points = self._fish_points


                # Draw the label
                self.draw_fish_point(this_point)

                # Don't pass on this touch
                return True
            elif self.drawing_state.mode is 'length':
                if self.drawing_state.first_touch.x < 0:
                    self.drawing_state.first_touch.x = touch.x
                    self.drawing_state.first_touch.y = touch.y

                    with self.canvas:
                        Color(1, 1, 0, 1)
                        d = dp(5)
                        Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                        # self.drawing_state.lines.append(Line(points=(touch.x, touch.y)))
                else:
                    new_point = (touch.x, touch.y)
                    first_point = (self.drawing_state.first_touch.x, self.drawing_state.first_touch.y)

                    self.drawing_state.first_touch.x = -1;
                    self.drawing_state.first_touch.y = -1;
                    self.drawing_state.mode = None

                    this_line = [first_point, new_point]
                    # Save this length / line
                    self.current_point.line = this_line

                    # Draw the line now.
                    self.draw_line(this_line)

                    # this is ugly...
                    self.current_point.organism_length = self.telem_entry['image_size_data'].get_distance_cm(
                        *this_line)

                    self.refresh()

            elif self.drawing_state.mode is 'area':
                if self.drawing_state.first_point is None:
                    self.drawing_state.first_point = (touch.x, touch.y)
                    self.drawing_state.poly_points = [self.drawing_state.first_point]

                    # Make the first dot large
                    with self.canvas:
                        Color(1, 1, 0, 1)
                        d = dp(12)
                        Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))# self.drawing_state.lines.append(Line(points=(touch.x, touch.y)))
                else:
                    new_point = (touch.x, touch.y)
                    self.drawing_state.poly_points.append(new_point)
                    first_point = self.drawing_state.first_point
                    # We have to do some checks.  We need 3 points for a polygon.  We close the polygon if we click on the start point
                    radius = dp(6)
                    distance_to_first = math.sqrt((new_point[0]-first_point[0])**2 + (new_point[1]-first_point[1])**2)
                    if (distance_to_first <= radius) and (len(self.drawing_state.poly_points) >= 3):
                        # close the polygon and save it.
                        self.drawing_state.mode = None
                        self.current_point.polygon = polygon_sort(self.drawing_state.poly_points)
                        self.drawing_state.poly_points = None
                        self.drawing_state.first_point = None
                        self.current_point.organism_area = self.telem_entry['image_size_data'].get_area_sq_cm(self.current_point.polygon)

                        # and refresh the screen
                        self.refresh()
                    else:
                        # Just extend the line.
                        # This actually draws an additional line every time we click a point, but we are going to clear it anyway.
                        with self.canvas:
                            Color(1, 1, 0, 1)
                            d = dp(4)
                            for point in self.drawing_state.poly_points:
                                Ellipse(pos=(point[0] - d / 2, point[1] - d / 2), size=(d, d))
                            Line(points=list(chain.from_iterable(self.drawing_state.poly_points)))




                    # touch.ud['line'] = Line(points=(touch.x, touch.y))
        return super(PaintWidget, self).on_touch_down(touch)



