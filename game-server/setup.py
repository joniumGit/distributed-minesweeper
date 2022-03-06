from distutils.core import setup

setup(
    name='ds-minesweeper-server',
    version='0.1.0',
    description='Simple Minesweeper Server',
    author='joniumGit',
    author_email='52005121+joniumGit@users.noreply.github.com',
    url='https://github.com/joniumGit/distributed-minesweeper',
    packages=['server'],
    package_dir={'': 'src/'},
    install_requires=[
        'fastapi >= 0.75.0'
        'ds-minesweeper',
        'httpheaders'
    ]
)
