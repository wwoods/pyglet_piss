from setuptools import setup, find_packages
import sys, os

if __name__ == '__main__':
    package = 'pyglet_piss'
    version = '0.0'
    
    setup(name = package,
          version = version,
          description = "Pyglet PISS - Player Input SystemS",
          long_description = """Framework for building games with pyglet""",
          classifiers = [],
          keywords = '',
          author = 'Walt Woods',
          author_email = 'woodswalben@gmail.com',
          url = 'https://github.com/wwoods/pyglet_piss',
          license = 'MIT',
          packages = find_packages(exclude = ['*.test', '*.test.*']),
          package_data = {},
          data_files = [],
          zip_safe = True,
          install_requires = [ 'pyglet', 'six' ],
          entry_points = """
          # -*- Entry points: -*-
          """
          )
    
    
