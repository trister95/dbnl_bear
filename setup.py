from setuptools import setup, find_packages

setup(
    name='dbnl_bear',
    version='0.3.1',
    packages=find_packages(),
    install_requires=["lxml", "tqdm", "python-dotenv", "langchain_core", "langchain_openai", "tqdm",
                      "typing", "langchain_text_splitters", "docx", "fuzzywuzzy", "pydantic",
                     "python-docx", "python-Levenshtein"],
    description='A Python package to use an AI assistant for historical analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Arjan van Dalfsen',
    author_email='j.a.vandalfsen@uu.nl',
    url='https://github.com/trister95/dbnl_bear',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
