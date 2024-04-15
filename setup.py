from setuptools import setup, find_packages

setup(
    name='real-time-language-translator',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition==3.8.1',
        'googletrans==4.0.0-rc1',
        'sounddevice==0.4.1',
        'gtts==2.2.3',
        'pygame==2.0.1',
        'streamlit==0.78.0'
    ],
)
