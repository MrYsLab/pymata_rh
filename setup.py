from setuptools import setup

with open('pypi_desc.md') as f:
    long_description = f.read()

setup(
    name='pymata_rh',
    version='1.2',
    packages=[
        'rh_tk_gui',
        'pymata_rh',
        'robohat_gateway'
    ],

    install_requires=[
        'python-banyan>=3.9',
        'pyserial'
    ],
    entry_points={
        'console_scripts': [
            'rhgui = rh_tk_gui.pymata_rh:vp_start_gui',
            'rhgw = robohat_gateway.robohat_gateway:robo_hat_gateway',
            'rhdemo = pymata_rh.rhgui:rhgui'
        ]
    },

    url='https://github.com/MrYsLab/pymata_rh',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    description='A Non-Blocking Event Driven Applications Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['python banyan', 'RPC', 'Remote Procedure Call', 'Event Driven',
              'Asynchronous', 'Non-Blocking',
              'Raspberry Pi', 'ZeroMQ', 'MessagePack'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Hardware'
    ],
)
