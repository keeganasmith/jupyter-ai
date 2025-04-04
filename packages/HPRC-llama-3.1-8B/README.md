# HPRC_llama_3.1_8B

`HPRC_llama_3.1_8B` is a Jupyter AI module, a package
that registers additional model providers and slash commands for the Jupyter AI
extension.

## Requirements

- Python 3.9 - 3.12
- JupyterLab 4

## Install

To install the extension, execute:

```bash
pip install HPRC_llama_3.1_8B
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall HPRC_llama_3.1_8B
```

## Contributing

### Development install

```bash
cd HPRC-llama-3.1-8B
pip install -e "."
```

### Development uninstall

```bash
pip uninstall HPRC_llama_3.1_8B
```

#### Backend tests

This package uses [Pytest](https://docs.pytest.org/) for Python testing.

Install test dependencies (needed only once):

```sh
cd HPRC-llama-3.1-8B
pip install -e ".[test]"
```

To execute them, run:

```sh
pytest -vv -r ap --cov HPRC_llama_3.1_8B
```
