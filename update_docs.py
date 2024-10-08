#! /usr/bin/env python3

"""
Run the commands to generate the installation, developer, and user manual.
Run the command to generate the HUGO website.

Start the following command from the project folder (make sure you are in the virtual environment):

    $ ./update_docs.py

"""

import subprocess
import textwrap

from pathlib import Path

import rich

HERE = Path(__file__).parent.resolve()

for folder, name in [
    ("installation", "installation-manual"),
    ("develop", "developer-manual"),
    ("user", "user-manual"),
    ("icd", "icd"),
    ("command", "commanding-manual"),
]:

    rich.print(f"Processing {name}: html.", end="", flush=True)
    subprocess.run(
        [
            f"asciidoctor "
            f"--require asciidoctor-tabs --out-file ../../docs/asciidocs/{name}.html {name}.adoc"
        ],
        cwd=HERE / f"src/{folder}",
        shell=True,
    )

    rich.print("..pdf", end="", flush=True)
    subprocess.run(
        [
            f"asciidoctor-pdf "
            f"--out-file ../../docs/pdfs/{name}.pdf {name}.adoc"
        ],
        cwd=HERE / f"src/{folder}",
        shell=True,
    )
    rich.print(".", flush=True)


rich.print("Updating the HUGO site..")
subprocess.run(["hugo"], cwd=HERE / "hugo")
rich.print("done.")

rich.print(textwrap.dedent(
    """
    [orange3]Warning:[/]
    At this point, you should fix the links for the documents in the `index.html` files: 
    
    * Remove the `../../` for all docs in the top-level `__index__.html`, i.e. 10 replacements.
    * Replace `../../` with `../` for all the docs in the  `__index__.html` of the `docs` folder, i.e. 11 replacements.  
    
    Eventually, I will automate this in this script.
    """
))
