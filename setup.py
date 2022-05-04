from setuptools import setup, find_packages

setup(
    name='pyqt-viewer-widget',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt viewer widget which helps you make viewer application easily',
    url='https://github.com/yjg30737/pyqt-viewer-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-toast>=0.0.1',
        'pyqt-fitting-graphics-view @ git+https://git@github.com/yjg30737/pyqt-fitting-graphics-view.git@main'
    ]
)