from setuptools import setup, find_packages

setup(name='tasks',
      description='Tasks management app',
      version='0.1',
      author='Me',
      author_email='me@email.com',
      url='github.com',
      packages=find_packages(where='src'),
      package_dir={'': 'src'}
      )
