from distutils.core import setup

setup(name='django-nanocms',
      version='0.1',
      description='Simple replacement for faltapages',
      author='Piotr Markiewicz',
      author_email='piotr.markiewicz@gmail.com',
      #url='http://code.google.com/p/django-contact-form/',
      packages=['nanocms'],
      classifiers=['Development Status :: 1 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      package_data={'nanocms': ['templates/*']},
      )
