import pandas as pd

from astro_engine.models import AstrologicalData, Body


def planets_table(chart: AstrologicalData):
    rows = []
    for name, b in chart.planets.bodies.items():
        rows.append(  # type: ignore
            {
                "Body": name,
                "Sign": b.sign,
                "DMS": f"{b.pos.deg:02d}°{b.pos.min:02d}'{b.pos.sec:05.2f}\"",
                "Lon": b.lon,
                "House": b.house,
                "Motion": b.motion,
                "Speed (deg/day)": b.speed_lon_deg_per_day,
            }
        )
    return pd.DataFrame(rows)


def houses_table(chart: AstrologicalData):
    rows = []

    def add_row(house_label: str, house: Body):
        rows.append(  # type: ignore
            {
                "House": house_label,
                "Sign": house.sign,
                "DMS": f"{house.pos.deg:02d}°{house.pos.min:02d}'{house.pos.sec:05.2f}\"",
                "Lon": house.lon,
            }
        )

    # --- Add angles first ---
    add_row("AC", chart.houses.asc)
    add_row("MC", chart.houses.mc)

    # --- Add house cusps ---
    for h, c in chart.houses.cusps.items():
        add_row(h, c)

    return pd.DataFrame(rows)


def aspects_table(chart: AstrologicalData):
    rows = []
    for a in chart.aspects:
        rows.append(  # type: ignore
            {
                "Body 1": a.body1,
                "Aspect": f"{a.aspect.symbol} ({a.aspect.name})",
                "Body 2": a.body2,
                "Orb": a.orb,
                "Phase": a.phase,
            }
        )
    return pd.DataFrame(rows)
