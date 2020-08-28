from setuptools import setup

setup(
    name='sssgen',
    version='0.4',
    description='Simple static site generator',
    url='https://github.com/edmund-huber/sssgen',
    license='MIT',
    zip_safe=False,
    scripts=['bin/sssgen'],
    packages=['sssgen'],
    install_requires=[
        'Mako==1.1.3',
        'MarkupSafe==1.1.1',
        'PyYAML==5.3.1',
        'argparse==1.4.0'
    ]
)
