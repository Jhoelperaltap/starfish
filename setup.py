from setuptools import setup, find_packages

setup(
    name='starfish',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Añadir dependencias aquí
    ],
    entry_points={
        'console_scripts': [
            'starfish=starfish.core.cli:main',
        ],
    },
)
