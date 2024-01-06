from pathlib import Path
import tomli
import tomli_w


def add_script(pyproject: Path, script_name: str, script_module_path: str) -> None:
    """adds a script to the pyproject.toml file"""

    if not pyproject.exists():
        raise FileNotFoundError(f"pyproject.toml file not found: {pyproject}")

    pyproject_contents = tomli.loads(pyproject.read_text())
    scripts = pyproject_contents["tool"]["poetry"]["scripts"]
    if script_name in scripts:
        raise ValueError(f"Script '{script_name}' already exists")
    scripts[script_name] = script_module_path

    pyproject.write_text(tomli_w.dumps(pyproject_contents))
