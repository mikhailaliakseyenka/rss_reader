from setuptools import setup

setup(
    name='rss_reader',
    version='1.4',
    author="Mikhail Aliakseyenka",
    author_email="aliakseyenkamikhail@gmail.com",
    packages=['src'],
    entry_points={
        'console_scripts': [
            'rss_reader = src:main',
        ]
    },
    include_package_data=True,
)