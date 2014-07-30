config_yaml = """# Generated GAE Deploy configuration file

# This is where custom frontend tools should be defined
project_base: '/Users/clmnbd/Projects/testing/testenv/project'

tools:
  build:
    command: 'grunt build'
  watch:
    command: 'grunt dev'

# You can define an arbitrary number of environments as required
# is_private flag will make all URLs in your app.yaml file to require an admin login
environments:
  production:
    application: ''
    path: '.production'
  staging:
    application: ''
    # is_private: true
    path: '.staging'
  development:
    application: ''
    path: ''
    preview: ''
    # watch should be relative to `path` so that we can pass this into Grunt as an option
    watch: ''

"""