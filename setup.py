from setuptools import setup

setup(
    name='sssgen',
    version='0.5',
    author='Edmund Huber',
    author_email='me@ehuber.info',
    description='Simple Static Site GENerator',
    url='https://github.com/edmund-huber/sssgen',
    license='MIT',
    zip_safe=False,
    scripts=['bin/sssgen'],
    packages=['sssgen'],
    install_requires=[
        'Mako==1.1.3',
        'MarkupSafe==1.1.1'
    ],
    python_requires='>=3.5'
)
