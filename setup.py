from setuptools import setup, find_packages
import os

version = '0.5'

setup(name='apyb.registration',
      version=version,
      description="Conference registration package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone apyb pythonbrasil web event conference',
      author='Erico Andrei <erico@simplesconsultoria.com.br>',
      author_email='products@simplesconsultoria.com.br',
      url='https://github.com/simplesconsultoria/apyb.registration',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['apyb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          # -*- Extra requirements: -*-
          'collective.autopermission',
          'collective.behavior.contactinfo==0.8',
          'collective.z3cform.datagridfield==0.7'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
