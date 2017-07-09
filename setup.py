from setuptools import find_packages, setup


def read_me():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except ImportError:
        return open('README.md', 'r').read()


setup(name='asserted',
      #version='0.0.1',
      description='pytest assert writer',
      long_description=read_me(),
      license='MIT',
      author='Hellowlol',
      author_email='hellowlol1@gmail.com',
      url='https://github.com/Hellowlol/asserted',
      #download_url='https://github.com/hellowlol/asserted/archive/0.0.1.tar.gz',
      packages=find_packages(exclude=['docs', 'tests*']),
      setup_requires=['pypandoc', 'setuptools_scm'],
      use_scm_version=True,
      #use_scm_version = {"root": "..", "relative_to": __file__},
      install_requires=[],
      python_requires='~=3.5',
      keywords='pytest, helper, automate',
      classifiers=[
                'Development Status :: 2 - Pre-Alpha',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.6', # Add more?


      ],
      entry_points={
        'console_scripts': [
            'asserted=asserted.cli:main',
        ]
    },

     )
