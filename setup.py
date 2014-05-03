from setuptools import setup

setup(
    name='sssgen',
    version='0.1',
    description='Simple static site generator',
    url='https://github.com/edmund-huber/sssgen',
    license='MIT',
    packages=[],
    zip_safe=False,
    scripts=['bin/sssgen'],
    install_requires=[
        'Mako==0.9.1',
        'PyYAML==3.11',
        'argparse==1.2.1'
    ]
)
