from setuptools import (
    find_packages,
    setup,
)

setup(
    name='pushalot',
    test_suite='tests',
    packages=find_packages(),
    version='0.1',
    description='',
    author='Alex Bo',
    author_email='bosha@the-bosha.ru',
    url='https://github.com/bosha/pypushalot',
    keywords=['pushalot', 'push', 'api'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)
