from setuptools import setup, find_packages

setup(
    name='ovadare',  
    version='0.1.0', 
    author='Oren Mukades', 
    author_email='ai@ovadare.com', 
    description='A framework for conflict detection and resolution in multi-agent systems.',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',  # Format of README
    url='https://github.com/nospecs/ovadare',  
    packages=find_packages(),  
    install_requires=[
        # Dependencies from requirements.txt
        "autogen>=0.2.0",
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
