import os
import sys
from setuptools import setup
from setuptools.command.develop import develop
from distutils import cmd

template = ['template', 'static']

share_voila_target = ['share', 'jupyter', 'voila', 'templates', 'ipypopout']


class DevelopCmd(develop):
    def run(self):
        if '--user' in sys.prefix:
            raise NotImplemented('--user not supported')

        link_target = os.path.join(sys.prefix, *share_voila_target)
        print('linking', os.path.abspath(template[0]), '->', link_target)
        os.symlink(os.path.abspath(template[0]), os.path.abspath(link_target))

        super(DevelopCmd, self).run()


class CleanDevelop(cmd.Command):
    user_options = []

    def finalize_options(self) -> None:
        pass

    def initialize_options(self) -> None:
        pass

    def run(self):
        os.unlink(os.path.join(sys.prefix, *share_voila_target))


def get_data_files(target, src):
    files = [(os.path.join(target, os.path.relpath(dirpath, src)),
              [os.path.join(dirpath, name) for name in filenames])
             for (dirpath, _, filenames) in os.walk(src)]
    return files


here = os.path.dirname(__file__)
version_ns = {}
with open(os.path.join(here, 'ipypopout', '_version.py')) as f:
    exec(f.read(), {}, version_ns)


setup(
    name='ipypopout',
    version=version_ns['__version__'],
    author='Mario Buikhuizen',
    author_email='mariobuikhuizen@gmail.com',
    url='https://github.com/mariobuikhuizen/ipypopout',
    packages=['ipypopout'],
    install_requires=[
        'ipywidgets>=7.7',
        'ipyvuetify>=1.7.0,<2',
    ],
    extras_require={
        "test": [
            "solara[pytest]",
        ],
        "voila": [
            "voila>=0.2.10,<0.5"
        ],
        "solara": [
            "solara>=1.36"
        ]
    },
    data_files=get_data_files(os.path.join(*share_voila_target), os.path.join(template[0])),
    cmdclass={
        'develop': DevelopCmd,
        'clean_develop': CleanDevelop
    }
)
