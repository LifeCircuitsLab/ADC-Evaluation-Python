#set page(paper:"a4")
#set text(font: "Arial")
#set par(justify: true, spacing: 1em)

#show title: set text(size: 17pt)
#show title: set align(center)
#title[ADC Evaluation Tool User Guide]

#align(center)[Life Circuits Lab @ HKUST]
#set heading(numbering: "1.1")
#show heading: set block(above: 1.5em, below: 1em)

= Getting started
This tool is intended to enable fast ADC prototyping at the behavior level. 
It is written in Python.
To run the script, you will need a working python installation, and corresponding dependencies.
Here is a quick example using "uv" for virtual environment management.

== Running this tool with uv

=== Installing uv

You can find the official documentation for uv at https://docs.astral.sh/uv/.
Follow the installation guide there.

=== Cloning the repository

To run the code, you need to first clone this repository by running the following command in your terminal:
```
git clone git@github.com:LifeCircuitsLab/ADC-Evaluation-Python.git
```

=== Setting up the virtual environment
Navigate to the cloned repository folder in the terminal.
Under it, run the following command:
```
uv venv --python="3.12.0"
uv sync
```

This will create a virtual environment with Python 3.12.0 and install all the dependencies specified in the `pyproject.toml` file.

=== Giving it a shot
With everything set, run:
```
uv run ./main.py
```

You should be all set.
