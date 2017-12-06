from setuptools import setup

setup(
    name = 'linter-html-server',
    version = '0.0.1',
    description = 'navigate in swarm of linter warnings',
    url = 'https://github.com/dfroger/linter-html',
    entry_points = {
        'console_scripts': [
            'linter-html-server = server:main',
            'linter-html-client = client:main',
        ],
    },
    license = 'GPL V3',
    author = 'David Froger',
    author_email = 'david.froger@mailoo.org',
    install_requires = ['aiohttp']
)
