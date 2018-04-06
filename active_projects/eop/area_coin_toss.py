from big_ol_pile_of_manim_imports import *
from eop.pascal import *


WIDTH = 12
HEIGHT = 1
GRADE_COLOR_1 = COLOR_HEADS = RED
GRADE_COLOR_2 = COLOR_TAILS = BLUE
NB_ROWS = 3


class Coin(Circle):
    CONFIG = {
        "radius": 0.2,
        "stroke_width": 3,
        "stroke_color": WHITE,
        "fill_opacity": 1,
        "symbol": "\euro",
    }

    def __init__(self, **kwargs):
        Circle.__init__(self,**kwargs)
        self.symbol_mob = TextMobject(self.symbol, stroke_color = self.stroke_color)
        self.symbol_mob.scale_to_fit_height(0.5*self.get_height()).move_to(self)
        self.add(self.symbol_mob)


class Heads(Coin):
    CONFIG = {
        "fill_color": COLOR_HEADS,
        "symbol": "H",
    }


class Tails(Coin):
    CONFIG = {
        "fill_color": COLOR_TAILS,
        "symbol": "T",
    }

class CoinStack(VGroup):
    CONFIG = {
        "spacing": 0.1,
        "size": 5,
        "face": Heads,
    }

    def generate_points(self):
        for n in range(self.size):
            coin = self.face()
            coin.shift(n * self.spacing * RIGHT)
            self.add(coin)

class HeadsStack(CoinStack):
    CONFIG = { "face": Heads }

class TailsStack(CoinStack):
    CONFIG = { "face": Tails }

class TallyStack(VGroup):

    def __init__(self,h,t,**kwargs):
        self.nb_heads = h
        self.nb_tails = t
        VGroup.__init__(self,**kwargs)

    def generate_points(self):
        stack1 = HeadsStack(size = self.nb_heads)
        stack2 = TailsStack(size = self.nb_tails)
        stack2.next_to(stack1, RIGHT, buff = SMALL_BUFF)
        self.add(stack1, stack2)


class AreaSplittingScene(Scene):

    def create_rect_row(self,n):
        rects_group = VGroup()
        for k in range(n+1):
            proportion = float(choose(n,k)) / 2**n
            new_rect = Rectangle(
                width = proportion * WIDTH, 
                height = HEIGHT,
                fill_color = graded_color(n,k),
                fill_opacity = 1
            )
            new_rect.next_to(rects_group,RIGHT,buff = 0)
            rects_group.add(new_rect)
        return rects_group

    def split_rect_row(self,rect_row):

        split_row = VGroup()
        for rect in rect_row.submobjects:
            half = rect.copy().stretch_in_place(0.5,0)
            left_half = half.next_to(rect.get_center(),LEFT,buff = 0)
            right_half = half.copy().next_to(rect.get_center(),RIGHT,buff = 0)
            split_row.add(left_half, right_half)
        return split_row

    def construct(self):

        # Draw the bricks

        brick_wall = VGroup()
        rect_row = self.create_rect_row(0)
        rect_row.move_to(3.5*UP + 0*HEIGHT*DOWN)
        self.add(rect_row)
        brick_wall.add(rect_row)
        brick_dict = {"0": {"0": rect_row.submobjects[0]}}

        for n in range(NB_ROWS):
            # copy and shift
            new_rect_row = rect_row.copy()
            self.add(new_rect_row)
            self.play(new_rect_row.shift,HEIGHT * DOWN)
            self.wait()

            #split
            split_row = self.split_rect_row(new_rect_row)
            self.play(FadeIn(split_row))
            self.remove(new_rect_row)
            self.wait()

            # merge
            rect_row = self.create_rect_row(n+1)
            rect_row.move_to(3.5*UP + (n+1)*HEIGHT*DOWN)
            self.play(FadeIn(rect_row))
            brick_wall.add(rect_row)
            self.remove(split_row)
            self.wait()

            # add to brick dict
            rect_dict = {}
            i = 0
            for rect in rect_row.submobjects:
                rect_dict[str(i)] = rect
                print "added rect for (", n+1, ",", i, ")"
                i += 1

            brick_dict[str(n+1)] = rect_dict


        for nrow_str,rect_row_dict in brick_dict.iteritems():
            for i_str, rect in rect_row_dict.iteritems():
                pos = rect.get_center()
                nrow = int(nrow_str)
                i = int(i_str)
                print nrow, i
                tally = TallyStack(nrow - i, i)
                tally.move_to(pos)
                self.add(tally)



        self.play(
            brick_wall.set_fill, {"opacity" : 0.2}
        )


        # Draw the branches

#            for n in NB_ROWS:






































        self.wait()



