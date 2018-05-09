from big_ol_pile_of_manim_imports import *
from active_projects.eop.reusable_imports import *
from active_projects.eop.independence import *

from for_3b1b_videos.pi_class import PiCreatureClass

class QuizResult(PiCreatureScene):
    CONFIG = {
        "pi_creatures_start_on_screen" : False,
        "random_seed" : 6
    }
    def construct(self):


        def get_example_quiz():
            quiz = get_quiz(
                "Define ``Brachistochrone'' ",
                "Define ``Tautochrone'' ",
                "Define ``Cycloid'' ",
            )
            rect = SurroundingRectangle(quiz, buff = 0)
            rect.set_fill(color = BLACK, opacity = 1)
            rect.set_stroke(width = 0)
            quiz.add_to_back(rect)
            return quiz


        highlight_color = WHITE

        nb_students_x = 5
        nb_students_y = 3
        spacing_students_x = 2.0
        spacing_students_y = 2.2

        all_students = PiCreatureClass(
            width = nb_students_x, height = nb_students_y)# VGroup()
        student_points = []
        grades = []
        grades_count = []
        hist_y_values = np.zeros(4)
        for i in range(nb_students_x):
            for j in range(nb_students_y):
                x = i * spacing_students_x
                y = j * spacing_students_y
                #pi = PiCreature().scale(0.3)
                #pi.move_to([x,y,0])
                #all_students.add(pi)
                all_students[i*nb_students_y + j].move_to([x,y,0])
                q1 = np.random.choice([True, False])
                q2 = np.random.choice([True, False])
                q3 = np.random.choice([True, False])
                student_points.append([q1, q2, q3])
                grade = q1*1+q2*1+q3*1
                grades.append(grade)
                hist_y_values[grade] += 1
                # How many times has this grade already occured?
                grade_count = grades.count(grade)
                grades_count.append(grade_count)


        all_students.move_to(ORIGIN)
        self.pi_creatures = all_students
        self.play(FadeIn(all_students))

        all_quizzes = VGroup()

        quiz = get_example_quiz().scale(0.2)
        for pi in all_students:
            quiz_copy = quiz.copy()
            quiz_copy.next_to(pi, UP)
            all_quizzes.add(quiz_copy)

        master_quiz = get_example_quiz()
        self.play(ShowCreation(master_quiz))
        self.play(Transform(master_quiz, all_quizzes[0]))

        self.play(LaggedStart(FadeIn,all_quizzes))

        grades_mob = VGroup()
        for (pi, quiz, grade) in zip(all_students, all_quizzes, grades):
            grade_mob = TexMobject(str(grade) + "/3")
            grade_mob.move_to(quiz)
            grades_mob.add(grade_mob)

        self.remove(master_quiz)
        self.play(
            FadeOut(all_quizzes),
            FadeIn(grades_mob)
        )

        # self.play(
        #     all_students[2:].fade, 0.8,
        #     grades_mob[2:].fade, 0.8
        # )

        students_points_mob = VGroup()
        for (pi, quiz, points) in zip(all_students, all_quizzes, student_points):
            slot = get_slot_group(points, include_qs = False)
            slot.scale(0.5).move_to(quiz)
            students_points_mob.add(slot)

        self.play(
            #all_students.fade, 0,
            FadeOut(grades_mob),
            FadeIn(students_points_mob)
        )



        anims = []
        anchor_point = 3 * DOWN + 1 * LEFT
        for (pi, grade, grades_count) in zip(all_students, grades, grades_count):
            anims.append(pi.move_to)
            anims.append(anchor_point + grade * RIGHT + grades_count * UP)
        anims.append(FadeOut(students_points_mob))

        self.play(*anims)

        grade_labels = VGroup()
        for i in range(4):
            grade_label = Integer(i, color = highlight_color)
            grade_label.move_to(i * RIGHT)
            grade_labels.add(grade_label)
        grade_labels.next_to(all_students, DOWN)
        out_of_label = TextMobject("out of 3", color = highlight_color)
        out_of_label.next_to(grade_labels, RIGHT, buff = MED_LARGE_BUFF)
        grade_labels.add(out_of_label)
        self.play(Write(grade_labels))

        grade_hist = Histogram(
            np.ones(4),
            hist_y_values,
            mode = "widths",
            x_labels = "none",
            y_label_position = "center",
            bar_stroke_width = 0,
            outline_stroke_width = 5
        )
        grade_hist.move_to(all_students)

        self.play(
            FadeIn(grade_hist),
            FadeOut(all_students)
        )


        nb_students_label = TextMobject("\# of students", color = highlight_color)
        nb_students_label.move_to(5 * LEFT + 2 * UP)
        arrows = VGroup(*[
            Arrow(nb_students_label.get_right(), grade_hist.bars[i].get_center(),
                color = highlight_color)
            for i in range(4)
        ])
        self.play(Write(nb_students_label), LaggedStart(GrowArrow,arrows))

        percentage_label = TextMobject("\% of students", color = highlight_color)
        percentage_label.move_to(nb_students_label)
        percentages = hist_y_values / (nb_students_x * nb_students_y) * 100
        anims = []
        for (label, percentage) in zip(grade_hist.y_labels_group, percentages):
            new_label = DecimalNumber(percentage,
                num_decimal_places = 1,
                unit = "\%",
                color = highlight_color
            )
            new_label.scale(0.7)
            new_label.move_to(label)
            anims.append(Transform(label, new_label))
        anims.append(ReplacementTransform(nb_students_label, percentage_label))
        self.play(*anims)

        self.remove(all_quizzes)
        # put small copy of class in corner
        for (i,pi) in enumerate(all_students):
            x = i % 5
            y = i / 5
            pi.move_to(x * RIGHT + y * UP)
        all_students.scale(0.8)
        all_students.to_corner(DOWN + LEFT)
        self.play(FadeIn(all_students))

        prob_label = TextMobject("probability", color = highlight_color)
        prob_label.move_to(percentage_label)
        self.play(
            all_students[8].set_color, MAROON_E,
            #all_students[:8].fade, 0.6,
            #all_students[9:].fade, 0.6,
            ReplacementTransform(percentage_label, prob_label)
        )

        self.play(
            FadeOut(prob_label),
            FadeOut(arrows)
        )

        flash_hist = FlashThroughHistogram(
                    grade_hist,
                    direction = "vertical",
                    mode = "random",
                    cell_opacity = 0.5,
                    run_time = 5,
                    rate_func = linear
                )

        flash_class = FlashThroughClass(
                    all_students,
                    mode = "random",
                    highlight_color = MAROON_E,
                    run_time = 5,
                    rate_func = linear
                )

        for i in range(3):
            self.play(flash_hist, flash_class)
            self.remove(flash_hist.prototype_cell)









