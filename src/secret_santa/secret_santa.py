import os
import click
import yaml
from graph import Vertex, Graph


@click.command()
@click.argument('config_file', type=click.File('rb'))
def secret_santa(config_file):
    """Generate a Secret santa following from the CONFIG_FILE."""
    root = os.path.dirname(os.path.abspath(__file__))
    config = yaml.safe_load(open(os.path.join(root, 'default.yml')))

    print("Creating a secret santa!")


if __name__ == '__main__':
    secret_santa()
