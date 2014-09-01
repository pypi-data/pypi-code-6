# Run the zetup script:
exec(open('__init__.py').read())


zetup(
  package_dir={
    'jinjatools.zetup': '.',
    },
  packages=[
    'jinjatools',
    'jinjatools.zetup',
    'jinjatools.django',
    'jinjatools.scons',
    ],
  package_data={
    'jinjatools.zetup': ZETUP_DATA,
    },
  )
