from setuptools import setup, find_packages


REQUIREMENTS = [
    'mysql-utilities==1.4.3',
]

TEST_REQUIREMENTS = [
    'coverage==3.7.1',
    'coveralls==0.5',
    'flake8==2.3.0',
    'mock==1.0.1',
]


EXCLUDE_FROM_PACKAGES = []


setup(
    name='dbcmonitor',
    version='0.1',
    url='https://github.com/TracyWebTech/dbcmonitor',
    author='Alexandre Barbosa',
    author_email='alexandrealmeidabarbosa@gmail.com',
    description='Database Replication Conflicts Monitor',
    license='LICENSE.txt',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests.run.run_with_coverage",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
