from distutils.core import setup
setup(
  name = 'dynamic_variables',
  packages = ['dynamic_variables'],
  version = '0.1',
  license='MIT',
  description = 'Change variables dynamically in runtime with the help of a simple GUI',
  author = 'Cahid Enes Keles',
  author_email = 'cahideneskeles54@gmail.com',
  url = 'https://github.com/cahidenes/dynamic_variables',
  download_url = 'https://github.com/cahidenes/dynamic_variables/archive/refs/tags/v_01.tar.gz',
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