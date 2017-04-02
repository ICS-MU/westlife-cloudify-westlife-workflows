import setuptools

setuptools.setup(
    zip_safe=False,
    name='cloudify-westlife-workflows',
    version='0.0.4',
    author='Vlastimil Holer',
    author_email='holer@ics.muni.cz',
    packages=['cloudify_westlife_workflows'],
    license='LICENSE',
    description='Cloudify West-Life plugin',
    install_requires=[
        'cloudify-plugins-common>=3.3.1'
    ],
)
