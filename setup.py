from distutils.core import setup

f = open("README.rst")

setup(
  name = 'dynamic_variables',
  version = '0.2.3',
  description = 'Change variables dynamically in runtime with the help of a simple GUI',
  long_description = f.read(),
  packages = ['dynamic_variables'],
  license='MIT',
  author = 'Cahid Enes Keles',
  author_email = 'cahideneskeles54@gmail.com',
  url = 'https://github.com/cahidenes/dynamic_variables',
  download_url = 'https://github.com/cahidenes/dynamic_variables/archive/refs/tags/v0.2.tar.gz',
  keywords = ['dynamic', 'variable', 'config', 'gui', 'change', 'runtime'],
  install_requires=[
          'tk',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
