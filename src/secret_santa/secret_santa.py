import os
import click
import yaml
from graph import Graph
from random import shuffle
from jinja2 import (Template, Environment, PackageLoader, FileSystemLoader,
                    select_autoescape)


class Participant:
    def __init__(self, name, group, email, lang='FR'):
        self.name = name
        self.group = group
        self.email = email

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


# Pascale                                                           Books - Livres
# Jonathan      Decoration - Objets de décoration, Electronics gadgets - Gadgets électroniques, Clothing accessories - Accessoires de vêtements Covfefe
# Charlène      Books - Livres, Cosmetics - Produits cosmétiques, Clothing accessories - Accessoires de vêtements
# Xiaoji        Decoration - Objets de décoration
# Joan          Books - Livres, Cosmetics - Produits cosmétiques, Clothing accessories - Accessoires de vêtements
# Vinciane      Books - Livres, Cosmetics - Produits cosmétiques, Beauty accessories - Accessoires de beauté, Clothing accessories - Accessoires de vêtements
# Vinciane      Books - Livres, Cosmetics - Produits cosmétiques, Beauty accessories - Accessoires de beauté, Clothing accessories - Accessoires de vêtements
# Christian     Books - Livres, Clothing accessories - Accessoires de vêtements, Food & Drink - A manger et à boire
# Jean-Luc      Food & Drink - A manger et à boire
# Bastien       Books - Livres, Electronics gadgets - Gadgets électroniques
# maxime        jeu steam peut être, id : troollcleans


def create_participants_list(people):
    return [
        Participant(
            name=p['name'], group=p['group'], email=p['email'], lang=p['lang'])
        for p in people
    ]


def graph_from(participants):
    g = Graph()

    for i in range(0, len(participants)):
        person = participants[i]
        nodelist = []

        for j in range(0, len(participants)):
            target = participants[j]
            if i != j and person.group != target.group:
                nodelist.append(j)

        g.add(i, person, nodelist)

    return g


@click.command()
@click.argument('config_file', type=click.File('rb'))
def secret_santa(config_file):
    """Generate a Secret santa following from the CONFIG_FILE."""
    root = os.path.dirname(os.path.abspath(__file__))
    config = yaml.safe_load(open(os.path.join(root, 'default.yml')))

    config_user = yaml.safe_load(config_file)
    config.update(config_user)

    template_dir = config.get('template_dir')
    if template_dir:
        loader = FileSystemLoader(template_dir)
    else:
        loader = PackageLoader('secret_santa', 'templates')

    env = Environment(
        loader=loader, autoescape=select_autoescape(['html', 'xml']))

    participants = create_participants_list(config['people'])
    shuffle(participants)
    G = graph_from(participants)
    order = G.hamiltonian()
    assignments = zip(order, order[1:] + [order[0]])
    for assignment in assignments:
        print(assignment[0].item.name + " -> " + assignment[1].item.name)

    template = env.get_template('email_en.html')
    print(template.render())


if __name__ == '__main__':
    secret_santa()
