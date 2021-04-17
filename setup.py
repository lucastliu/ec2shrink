from setuptools import setup

setup(
  name='ec2shrink',
  packages=['ec2shrink'],
  version='1.0.2',
  license='GPLv3',
  description='An easier way to reduce the storage size for EC2.',
  long_description='AWS CLoudShell CLI tool intended to make shrinking EC2 EBS Storage easier',
  long_description_content_type='text/plain',
  author='Lucas Liu',
  author_email='lucas.liu.0000@gmail.com',
  url='https://github.com/lucastliu/ec2shrink',
  download_url='https://github.com/lucastliu/ec2shrink/archive/pypi-0_1_3.tar.gz',
  keywords=['amazon', 'aws', 'ec2', 'storage'],
  install_requires=[
          'awscli',
          'ec2instanceconnectcli',
          'click',
          'pexpect',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',

    'Programming Language :: Python :: 3',
  ],
  entry_points={
        "console_scripts": [
            "ec2shrink=ec2shrink.__main__:main",
        ]
    },
)
