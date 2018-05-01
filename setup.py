import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as license:
    LICENSE = license.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='image_color_analysis',
      version='1.0',
      install_requires=['Pillow>=5.1.0', 'sklearn>=0.0', 'numpy>=1.14.3', 'scipy>=1.0.1'],
      include_package_data=True,
      license=LICENSE,  # example license
      description='image color analysis',
      long_description=README,
      packages=[],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: Other/Proprietary License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
      ],
      # author='Yael Segal',
      # author_email='devorawitty@chelem.co.il',
      zip_safe=False)

