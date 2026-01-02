# Astro render


A second iteration of astro engine but this time it contains a finction to render graph. 

This one showcases the graphical astrological chart. 

This is the secodn iteration of Astro Engine, more will follow. 


### Virtual environment (recommended)

It is strongly recommended to run Astro-Engine inside a Python virtual environment.

A virtual environment:
- keeps project dependencies isolated
- avoids conflicts with system-wide Python packages
- makes the project easier to reproduce and maintain

The Makefile in this repository does **not** create or activate a virtual environment automatically.

Before using the project, please create and activate a virtual environment using standard Python tooling, for example:

```bash
python -m venv venv
source venv/bin/activate
```

If you prefer, you may also install dependencies and run the commands without a virtual environment, but this is not recommended.

### Install dependencies

This project uses a Makefile that automatically creates a virtual environment and installs dependencies.

```bash
make install
```

---

## Usage

Run unit tests

```bash
make test
```

Run the example script (programmatic usage)

```bash
make example
```

Run the demo interface (Streamlit)

```bash
make demo
```

The Streamlit app will open in your browser and allows interactive chart calculation and table rendering.


Clean cache files:

```bash
make clean
```

### Windows users

Astro-Engine itself is fully compatible with Windows.

The provided Makefile targets are intended for macOS and Linux environments.
Windows users can either:

- use WSL or Git Bash, or
- run the commands manually using standard Python tooling:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest
python example.py
streamlit run demo.py
```

## Output

Astro-Engine outputs chart data as structured JSON, including:

- metadata (time, timezone, Julian date)
- planetary positions and motion
- house cusps, ASC and MC
- major aspects with orbs and phases

This makes the engine suitable as a data layer for other applications.

## License

MIT License


This software uses Swiss Ephemeris

© Astrodienst AG

Licensed under the Swiss Ephemeris Free License