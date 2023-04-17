from setuptools import setup, find_packages

setup(
    name='americanthesis',
    version='0.0.1',
    url='https://github.com/danielsuo/americanthesis',
    author='Daniel Suo',
    author_email='danielsuo@gmail.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=[
        'numpy >= 1.11.1',
        'beautifulsoup4',
        'matplotlib >= 1.5.1',
        'absl-py',
        'immutabledict',
        'pandas',
        'jupyter',
        'ipython',
        'requests',
    ],
)
