from setuptools import setup, find_packages

setup(
    name = 'todoapi',
    version = '0.1',
    packages = find_packages(),
    install_requires = [
        'SQLAlchemy==0.9.1',
        'Flask==0.10',
        'Flask-SQLAlchemy==1.0  '
        ],
    setup_requires=[
        ],
    # metadata for upload to PyPI
    author = 'Matthew Peddle',
    author_email = 'matthew.t.peddle@gmail.com',
    description = 'Simple todo API',
    long_description = '''Simple todo API
    ''',
    include_package_data = True,
    entry_points = '''
    '''
)
