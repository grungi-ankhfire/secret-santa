import os
import click
import yaml
from graph import Graph
from random import shuffle
from jinja2 import (Environment, PackageLoader, FileSystemLoader,
                    select_autoescape)


class Participant:
    def __init__(self, name, group, email, gifts, lang='FR'):
        self.name = name
        self.group = group
        self.email = email
        self.lang = lang
        self.gifts = gifts

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def create_participants_list(people):
    return [
        Participant(
            name=p['name'],
            group=p['group'],
            email=p['email'],
            gifts=p.get('gifts'),
            lang=p['lang']) for p in people
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


def render_email(env, giver, giftee):
    lang = giver.lang.lower()
    template = env.get_template(lang + '/email.html')
    print(template.render(giver=giver, giftee=giftee))


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
        render_email(env, giver=assignment[0].item, giftee=assignment[1].item)


if __name__ == '__main__':
    secret_santa()
