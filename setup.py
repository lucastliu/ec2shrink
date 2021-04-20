from setuptools import setup

setup(
  name='ec2shrink',
  packages=['ec2shrink'],
  version='1.1.0',
  license='GPLv3',
  description='An easier way to reduce the storage size for EC2.',
  long_description='CLI tool intended to make shrinking EC2 EBS Storage easier',
  long_description_content_type='text/plain',
  author='Lucas Liu',
  author_email='lucas.liu.0000@gmail.com',
  url='https://github.com/lucastliu/ec2shrink',
  keywords=['amazon', 'aws', 'ec2', 'storage'],
  install_requires=[
          'ec2instanceconnectcli',
          'click',
          'pexpect',
          # 'awscli'  # do not use this for AWS CloudShell release, only for other devices
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
