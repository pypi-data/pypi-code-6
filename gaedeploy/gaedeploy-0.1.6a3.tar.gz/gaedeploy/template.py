config_yaml = """# Generated GAE Deploy configuration file

# This is where custom frontend tools should be defined
tools:
  build:
    command: "grunt build"
    path: ""

# You can define an arbitrary number of environments as required
# is_private flag will make all URLs in your app.yaml file to require an admin login
environments:
  production:
    application: ""
    path: ".production"
  staging:
    application: ""
    path: ".staging"
    is_private: true

"""