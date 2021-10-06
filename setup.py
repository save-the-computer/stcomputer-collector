from setuptools import setup, find_packages
import stcomputer_collector

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='stcomputer-collector',
    version=stcomputer_collector.__version__,
    description='Collector that collect product data from external providers such as danawa',
    author=stcomputer_collector.__author__,
    author_email='solo_5@naver.com',
    url='https://github.com/save-the-computer/collector',
    download_url='https://github.com/save-the-computer/collector/archive/0.1.0.tar.gz',
    install_requires=requires,
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires='>=3',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
