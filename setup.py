from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def version():
    with open('VERSION', 'r') as f:
        return f.read().rstrip()


setup(
    name='neobrainfuck',
    version=version(),
    author='kusrabyzarc',
    author_email='crazybarsuk@mail.ru',
    description='Just another rethink of the BrainFuck language',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/kusrabyzarc/NeoBrainF--k',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='BrainFuck interpreter extended programming language esolang development python library brainfuck-interpreter esoteric extended-brainfuck',
    project_urls={},
    python_requires='>=3.10'
)
