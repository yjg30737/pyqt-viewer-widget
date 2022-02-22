from setuptools import setup, find_packages

setup(
    name='pyqt-viewer-widget',
    version='0.3.0',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt Viewer Widget',
    url='https://github.com/yjg30737/pyqt-viewer-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'Pillow>=9.0.0',
        'pyqt-toast @ git+https://git@github.com/yjg30737/pyqt-toast.git@main',
        'pyqt-fitting-graphics-view @ git+https://git@github.com/yjg30737/pyqt-fitting-graphics-view.git@main'
    ]
)