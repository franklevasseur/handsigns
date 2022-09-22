import click

from . import datacollect as dc, predict as pr, train as tr


@click.command()
@click.option('--data-dest', help='Path to save data')
def collect(dest: str):
    """Collect Data for a a given label."""
    dc.collect(dest)


@click.command()
@click.option('--data-dir', help='Path to data directory')
@click.option('--model-dest', help='Path to the trained model')
def train(data_dir: str, model_dest: str):
    """Train a model."""
    tr.train(data_dir, model_dest)


@click.command()
@click.option('--model-path', help='Path to trained model')
def predict(model_path: str):
    """Predict in realtime."""
    pr.predict(model_path)


@click.group()
def group():
    pass


group.add_command(collect)
group.add_command(train)
group.add_command(predict)

if __name__ == '__main__':
    group()
