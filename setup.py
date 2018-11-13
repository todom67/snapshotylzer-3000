from setuptools import setup

setup(
    name='snapshotylyzer-3000',
    version='0.1',
    author="Timothy Odom",
    author_email="todom67@gmail.com",
    description="A tool to manage AWS EC2 snapshots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/todom67/snapshotylzer-3000",
    install_requires=[
        'click',
        'boto3',
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)