from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any, Literal
import matplotlib.pyplot as plt


class Side:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Side) -> Side:
        return Side(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Side) -> Side:
        return Side(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Side:
        return Side(self.x * scalar, self.y * scalar)

    def __div__(self, scalar: float) -> Side:
        return Side(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"{self.x},{self.y}"

    def __eq__(self, other: Side):
        return self.x == other.x and self.y == other.y


@dataclass
class Color:
    name: str


class Car:
    def __init__(self, coming_from: Side, going_to: Side, color: Color):
        self.coming_from: Side = coming_from
        self.going_to: Side = going_to
        self.color: Color = color

        eps = 0.1
        delta = 0.2
        if self.coming_from == Side(0, 1):
            path = [Side(-eps, 1), Side(-eps, delta)]
        elif self.coming_from == Side(1, 0):
            path = [Side(1, eps), Side(delta, eps)]
        elif self.coming_from == Side(0, -1):
            path = [Side(eps, -1), Side(eps, -delta)]
        else:
            path = [Side(-1, -eps), Side(-delta, -eps)]

        if self.going_to == Side(0, 1):
            path.extend([Side(eps, delta), Side(eps, 1)])
        elif self.going_to == Side(1, 0):
            path.extend([Side(delta, -eps), Side(1, -eps)])
        elif self.going_to == Side(0, -1):
            path.extend([Side(-eps, -delta), Side(-eps, -1)])
        else:
            path.extend([Side(-delta, eps), Side(-1, eps)])
        self.path = path

    def __repr__(self):
        return f"{self.color}, {self.coming_from}, {self.going_to}, {self.path}"


all_sides = [Side(0, 1), Side(1, 0), Side(0, -1), Side(-1, 0)]
all_colors: list[Color] = [Color("red"), Color("blue"), Color("orange"), Color("green")]


class Sign:
    def __init__(self, n_sides: Literal[2, 3, 4], n_cars: Literal[2, 3, 4]) -> None:
        self.sides = random.sample(all_sides, n_sides)
        self.vorfahrt = random.sample(self.sides, 2)

        if n_cars > n_sides:
            raise ValueError("Number of cars must be smaller than number of sides.")

        self.cars: list[Car] = []
        colors = random.sample(all_colors, n_cars)
        incoming_directions = random.sample(self.sides, n_cars)
        for color, coming_from in zip(colors, incoming_directions, strict=True):
            while True:
                going_to = random.choice(self.sides)
                if going_to != coming_from:
                    break
            self.cars.append(
                Car(coming_from=coming_from, going_to=going_to, color=color)
            )

    def draw(
        self,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
    ):
        if subplot_kwargs is None:
            subplot_kwargs = {"figsize": (2 * 4, 4)}
        if plot_kwargs is None:
            plot_kwargs = {
                "color": "black",
                "linewidth": 30.0,
            }

        center = Side(0, 0)
        fig, axs = plt.subplots(1, 2, **subplot_kwargs)

        # Traffic sign
        ax = axs[0]
        for side in self.sides:
            draw_till = (side + center) * 0.5
            ax.plot([side.x, draw_till.x], [side.y, draw_till.y], **plot_kwargs)

        ax.plot([self.vorfahrt[0].x, 0], [self.vorfahrt[0].y, 0], **plot_kwargs)
        ax.plot([self.vorfahrt[1].x, 0], [self.vorfahrt[1].y, 0], **plot_kwargs)
        ax.set(xlim=(-1, 1), ylim=(-1, 1), xticks=[], yticks=[], aspect="equal")
        ax.set_title("Traffic Sign")
        # Road
        ax = axs[1]
        ax.set_title("Cars")

        for side in self.sides:
            ax.plot(
                [side.x, center.x],
                [side.y, center.y],
                color="lightgray",
                linewidth=plot_kwargs["linewidth"],
                zorder=1,
            )

        for style, car in zip(["-", "--", ":", "-."], self.cars, strict=False):
            ax.scatter(
                car.path[0].x,
                car.path[0].y,
                color=car.color.name,
                s=500,
                zorder=2,
            )

            ax.plot(
                [p.x for p in car.path],
                [p.y for p in car.path],
                color=car.color.name,
                linestyle=style,
                linewidth=8,
            )

            # w = 0.2
            # almost_center_from = (car.coming_from * w) + (center * (1 - w))
            # ax.plot(
            #     [car.coming_from.x, almost_center_from.x],
            #     [car.coming_from.y, almost_center_from.y],
            #     "--",
            #     color=car.color.name,
            #     alpha=1,
            #     linewidth=4,
            # )
            # almost_center_to = (car.going_to * w) + (center * (1 - w))

            # ax.plot(
            #     [car.going_to.x, almost_center_to.x],
            #     [car.going_to.y, almost_center_to.y],
            #     "--",
            #     color=car.color.name,
            #     alpha=1,
            #     linewidth=4,
            # )
            # ax.plot(
            #     [almost_center_from.x, almost_center_to.x],
            #     [almost_center_from.y, almost_center_to.y],
            #     "-",
            #     color=car.color.name,
            #     alpha=1,
            #     linewidth=4,
            # )
        eps = 0.1
        ax.set(
            xlim=(-1 - eps, 1 + eps),
            ylim=(-1 - eps, 1 + eps),
            xticks=[],
            yticks=[],
            aspect="equal",
        )
        return fig
