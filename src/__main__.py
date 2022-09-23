import pathlib as pl

import click
import questionary as q
from click_default_group import DefaultGroup

from . import datacollect as dc, logger as log, predict as pr, train as tr

CWD = pl.Path.cwd()
DEFAULT_DATA_DIR = CWD / "data"
DEFAULT_MODEL_FILE = CWD / "model.pkl"

logger = log.Logger()


def assert_dir(dir_path: str):
    path = pl.Path(dir_path)
    if not path.exists():
        raise click.BadParameter(f"Path {path} does not exist")
    if not path.is_dir():
        raise click.BadParameter(f"Path {path} is not a directory")


@click.group(cls=DefaultGroup, default="menu", default_if_no_args=True)
def cli():
    pass


@cli.command()
@click.option('--data-dir', help='Path to data directory', default=DEFAULT_DATA_DIR)
@click.option('--label', help='Path to save data', prompt=True)
def collect(data_dir: str, label: str):
    """Collect Data for a a given label."""
    assert_dir(data_dir)
    data_dest = pl.Path(data_dir) / f"{label}.csv"
    dc.collect(data_dest, logger)


@cli.command()
@click.option('--data-dir', help='Path to data directory', default=DEFAULT_DATA_DIR)
@click.option('--model', help='Path to the trained model', default=DEFAULT_MODEL_FILE)
def train(data_dir: str, model: str):
    """Train the model for later use at predict time."""
    assert_dir(data_dir)
    tr.train(pl.Path(data_dir), pl.Path(model), logger)


@cli.command()
@click.option('--model', help='Path to trained model', default=DEFAULT_MODEL_FILE)
def predict(model: str):
    """Predict in realtime."""
    pr.predict(pl.Path(model), logger)


@cli.command()
def menu():
    """Launch the menu."""
    choices = ['collect', 'train', 'predict']
    choice = q.select('What do you want to do?', choices=choices).ask()
    if choice == 'collect':
        collect()
    elif choice == 'train':
        train()
    elif choice == 'predict':
        predict()
    else:
        logger.info("Goodbye!")
        return


if __name__ == '__main__':
    cli()
