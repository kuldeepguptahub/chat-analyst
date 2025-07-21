from setuptools import setup, find_packages

setup(
    name= 'chat-analyst',
    version= '1.0.0.',
    description= 'An LLM powered chat QA analyst for support chat evaluation',
    author= 'Kuldeep Gupta',
    author_email='kuldeep.gupta2603@gmail.com',
    packages=find_packages(include=['src', 'llm_engine', 'schemas', 'prompts', 'models']),
    include_package_data=True,
    install_requires= [
        'stearmlit',
        'python-dotenv',
        'together'
    ],
    classifiers=[
        'Programming Language :: Python 3',
        'License :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>3.8'
)