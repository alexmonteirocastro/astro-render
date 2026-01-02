from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from astro_engine.models import AstrologicalData, Body

SIGN_GLYPHS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]


def render_zodiac_wheel(*, title: str = "Zodiac Wheel", asc_lon: float = 0.0):
    outer_r = 1.0
    inner_r = 0.72
    """
    Draw zodiac wheel (sign ring only), oriented so the Ascendant is at 9 o'clock.

    Fixed convention:
      - 0° in our polar plot is at 9 o'clock (we use theta_zero_location('W'))
      - angles increase counter-clockwise

    asc_lon:
      Ascendant longitude in absolute zodiac degrees (0..360, 0=Aries).
      We rotate the entire sign ring by -asc_lon so ASC appears at 9 o'clock.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection="polar")

    # Your fixed wheel convention
    ax.set_theta_zero_location("W")  # 0° at 9 o'clock
    ax.set_theta_direction(1)  # counter-clockwise

    label_r = 0.86
    boundary_lw = 1.2
    ring_lw = 2.0

    ax.set_ylim(0, outer_r * 1.3)
    ax.spines["polar"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["polar"].set_linewidth(ring_lw)

    thetas = np.linspace(0, 2 * np.pi, 720)
    ax.plot(thetas, np.full_like(thetas, outer_r), color="black", lw=ring_lw)
    ax.plot(thetas, np.full_like(thetas, inner_r), color="black", lw=boundary_lw)

    # Rotation offset: rotate the whole zodiac ring so ASC becomes 0° at 9 o'clock
    offset = (-float(asc_lon)) % 360.0

    def theta_deg(lon_deg: float) -> float:
        """Convert a zodiac longitude to polar theta (radians), including wheel rotation."""
        return np.deg2rad((lon_deg + offset) % 360.0)

    # Draw sign boundaries + labels, rotated
    for i in range(12):
        boundary_lon = i * 30.0
        mid_lon = i * 30.0 + 15.0

        th_b = theta_deg(boundary_lon)
        ax.plot([th_b, th_b], [inner_r, outer_r], color="black", lw=boundary_lw)

        th_m = theta_deg(mid_lon)
        ax.text(th_m, label_r, SIGN_GLYPHS[i], fontsize=22, ha="center", va="center")

    ax.set_title(title, pad=20, fontsize=14)
    plt.tight_layout()
    return fig, ax


def draw_marker(
    ax,
    marker: Body,
    marker_name: str,
    *,
    inner_r: float = 0.72,
    outer_r: float = 1.0,
    label_r: float = 0.68,
    color: str = "crimson",
    lw: float = 2.5,
):
    """
    Draw marker on an existing polar axis.
    Expects rising like:
      {'sign':'Leo', 'pos': {...}, 'lon': 128.669126}

    Assumes the axis has already been configured with the desired orientation
    (theta zero location and direction). We only need theta = radians(lon).
    """
    lon = float(marker.lon) % 360.0
    theta = np.deg2rad(lon)

    # Main marker line
    ax.plot([theta, theta], [inner_r, outer_r], color=color, lw=lw, zorder=20)

    # A small arrow-ish triangle near the outer ring (optional flair)
    # You can remove this block if you want it simpler.
    tip_r = outer_r + 0.1
    base_r = outer_r - 0.05
    spread = np.deg2rad(1.2)  # angle spread for the triangle
    ax.fill(
        [theta, theta - spread, theta + spread],
        [tip_r, base_r, base_r],
        color=color,
        alpha=0.9,
        zorder=21,
    )

    # Label
    sign = marker.sign
    pos = marker.pos
    deg = marker.pos.deg
    minute = marker.pos.min
    label = f"{marker_name} {sign} {deg}°{minute}'" if sign else f"{marker_name}"
    ax.text(
        theta,
        label_r,
        label,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=color,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85),
        zorder=22,
    )


import numpy as np


def draw_cusp(
    ax,
    cusp: Body,
    cusp_name: str,
    *,
    inner_r: float = 0.72,
    label_r: float = 0.42,
    color: str = "black",
    lw: float = 0.9,
    show_label: bool = True,
):
    """
    Draw a house cusp (thin black line) on an existing polar axis.

    - Line goes from center (r=0) to outer ring (r=outer_r)
    - No arrow head
    - Uses same theta logic as draw_marker(): theta = radians(lon)

    cusp: Body with .lon (degrees), optionally .sign/.pos if you want labels
    cusp_name: e.g. "1", "2", ..., "12" or "I"..."XII"
    """
    lon = float(cusp.lon) % 360.0
    theta = np.deg2rad(lon)

    # Thin cusp line from center to inner ring
    ax.plot([theta, theta], [0.0, inner_r], color=color, lw=lw, zorder=10)

    if show_label:
        ax.text(
            theta,
            label_r,
            str(cusp_name),
            ha="center",
            va="center",
            fontsize=9,
            color=color,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75),
            zorder=11,
        )


PLANET_ORDER = [
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "True N.Node",
    "True S.Node",
]

PLANET_GLYPHS = {
    "Sun": "☉",
    "Moon": "☽",
    "Mercury": "☿",
    "Venus": "♀",
    "Mars": "♂",
    "Jupiter": "♃",
    "Saturn": "♄",
    "Uranus": "♅",
    "Neptune": "♆",
    "Pluto": "♇",
    "True N.Node": "☊",
    "True S.Node": "☋",
}


def draw_planet(
    ax,
    planet: Body,
    planet_name: str,
    *,
    line_start_r: float = 1.0,  # start at wheel edge
    line_end_r: float = 1.12,  # extend outside the wheel
    glyph_r: float = 1.18,  # glyph position (outside)
    color: str = "black",
    lw: float = 1.0,
    fontsize: int = 16,
):
    """
    Draw a planet outside the wheel with a leader line from the wheel edge.

    Assumes planet.lon is already in the same rotated coordinate system as the wheel.
    """
    lon = float(planet.lon) % 360.0
    theta = np.deg2rad(lon)

    # Leader line from the wheel edge outward
    ax.plot([theta, theta], [line_start_r, line_end_r], color=color, lw=lw, zorder=30)

    # Glyph at the end (outside the wheel)
    glyph = PLANET_GLYPHS.get(planet_name, planet_name[:2])

    ax.text(
        theta,
        glyph_r,
        glyph,
        fontsize=fontsize,
        ha="center",
        va="center",
        color=color,
        zorder=31,
    )


def _rotate_lon(lon: float, asc_lon: float) -> float:
    """Rotate a longitude so ASC becomes 0°."""
    return (float(lon) - float(asc_lon)) % 360.0


def rotate_chart_data_to_asc(astro_data: AstrologicalData) -> AstrologicalData:
    """
    Returns a deep-copied dict where all longitudes are rotated so ASC is 0°.
    Adjust the places we iterate if your schema differs.
    """
    d = deepcopy(astro_data)
    asc_lon = d.houses.asc.lon

    # Rotate ASC itself (becomes 0 by definition)
    d.houses.asc.lon = _rotate_lon(d.houses.asc.lon, asc_lon)
    # Rotate MC
    d.houses.mc.lon = _rotate_lon(d.houses.mc.lon, asc_lon)

    # Rotates the cusps of the houses
    for house_cusp in d.houses.cusps.values():
        house_cusp.lon = _rotate_lon(house_cusp.lon, asc_lon)

    # Rotates the planets
    for planet in d.planets.bodies.values():
        planet.lon = _rotate_lon(planet.lon, asc_lon)

    return d


def render_astrological_chart(
    data: AstrologicalData,
    title: str = "Astrological Chart",
):
    # Rotate the wheel so rising is now 0° and rotate the chart data to align
    rotated_data = rotate_chart_data_to_asc(data)

    rotated_rising = rotated_data.houses.asc
    rotated_midheaven = rotated_data.houses.mc

    fig, ax = render_zodiac_wheel(
        title=title,
        asc_lon=data.houses.asc.lon,
    )

    draw_marker(ax, rotated_rising, "ASC", inner_r=0.72, outer_r=1.0)
    draw_marker(ax, rotated_midheaven, "MC", inner_r=0.72, outer_r=1.0)
    for house in rotated_data.houses.cusps.keys():
        draw_cusp(ax, rotated_data.houses.cusps[house], house)

    i = 0
    for planet in rotated_data.planets.bodies.keys():
        i += 1
        if planet not in ["Mean N.Node", "Mean S.Node"]:
            draw_planet(
                ax,
                rotated_data.planets.bodies[planet],
                planet,
                color=f"{'red' if rotated_data.planets.bodies[planet].motion == 'RETRO' else 'black'}",
                # TODO Handle rendering of conjuect planets better
                # line_end_r=1.12 if i // 2 == 0 else 1.18,
                # glyph_r=1.18 if i // 2 == 0 else 1.24,
            )

    return fig
