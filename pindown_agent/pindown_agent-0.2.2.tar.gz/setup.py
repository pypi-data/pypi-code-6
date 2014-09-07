from setuptools import setup

setup(
    name='pindown_agent',
    license="BSD",
    version='0.2.2',
    long_description=__doc__,
    packages=['pindown_agent'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'tornado', 'supervisor', 'python-keyczar'],
    author_email='aybars.badur@gmail.com',
    author = 'ybrs',
    url = 'https://pindown.io/',
    entry_points = {
        'console_scripts': [
            'pindown_agent = pindown_agent.client:client',
            'pindown_agent_setup = pindown_agent.app:setup',
            'pindown_agent_run = pindown_agent.app:run_supervisor',
            'pindown_agent_stop = pindown_agent.app:stop_agent',
            'pindown_agent_start = pindown_agent.app:start_agent',
            'pindown_agent_restart = pindown_agent.app:restart_agent',
            'pindown_agent_status = pindown_agent.app:agent_status',
            'pindown_agent_add_project = pindown_agent.app:add_project',
        ],
    }
)
