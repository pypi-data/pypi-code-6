"""
Stop most services from starting
================================

Some Debian package installs automatically launch a daemon, and sometimes you
don't want that to happen immediately. :code:`stopstartup`, when activated,
will stop any service started via :code:`invoke-rc.d` from starting. It does
this by hijacking :code:`/usr/sbin/policy-rc.d`, which :code:`invoke-rc.d`
calls for every service.  Normally the file should determine if your currently
active "policy" (whatever that means) should allow the service to startup. The
policy enforcer installed by :code:`stopstartup` is much less nice, and simply
rejects any request.

The policy is installed at :code:`usr/sbin/`, so if you don't have proper
permissions there you'll be unable to run :code:`stopstartup`. If that happens,
try using :code:`sudo`.
"""
from click import group, echo, style, pass_context, make_pass_decorator
from collections import namedtuple


State = namedtuple("State", ("home", "install_dir"))
pass_state = make_pass_decorator(State)

@group()
@pass_context
def cli(ctx):
    """
    Packages that install a service and then automatically execute it are
    annoying. Why deal with it? Why not just take advantage of the fact that
    LSB compliant packages must use invoke-rc.d to start these services, and
    that invoke-rc.d defers to /usr/sbin/policy-rc.d?


    Calling start will replace the current policy enforcer at
    /usr/sbin/policy-rc.d with a custom one that will reject every request.
    
    Calling stop will remove the custom enforcer, and will put your old
    enforcer back in place, assuming you had one.
    """
    from os.path import join
    home = join("/", "usr", "local", "stopstartup")
    install_dir = join("/", "usr", "sbin")
    ctx.obj = State(home, install_dir)

def exists(path):
    """
    Determine if a path is:
    1. a link
    2. a file
    3. a directory
    """
    from os.path import isfile, islink, isdir
    return isfile(path) or islink(path) or isdir(path)

def are_the_same(first, second):
    """
    Determine if two paths point to the same thing.
    Symbolic links will be followed to the very end.
    """
    from os.path import realpath
    return realpath(first) == realpath(second)

def broken():
    echo(style("BROKEN!", fg = "white", bg = "red", blink = True))

def active():
    echo(style("ACTIVE", fg = "red", blink = True))

def inactive():
    echo(style("INACTIVE", fg = "green", blink = True))

def require_elevated_privileges(f):
    from functools import update_wrapper
    @pass_context
    def new_func(context, *args, **kwargs):
        try:
            return context.invoke(f, *args, **kwargs)
        except (OSError, IOError):
            echo(style("ELEVATE ME", fg = "cyan", blink = True))
            echo("Try using sudo")
            exit(1)
    return update_wrapper(new_func, f)

@cli.command()
@require_elevated_privileges
@pass_state
def start(state):
    """
    Start stopping services from starting.

    Any existing policy enforcer will be sidelined. You must call stop to undo
    the sidelining. It is also not recommended that you manually replace the
    installed policy enforcer after calling start and before calling stop;
    doing so may cause your original policy enforcer to be overwritten during
    the sidelining process.
    """
    from os import symlink
    from os.path import join
    from shutil import move
    source = join(state.home, "policy-rc.d")
    destination = join(state.install_dir, "policy-rc.d")
    sideline = join(state.install_dir, "policy-rc.d.sidelined")
    if are_the_same(source, destination):
        echo("Stopping has already been started!")
        exit(1)
    if exists(destination):
        move(destination, sideline)
        echo("A policy enforcer existed, and was sidelined")
    symlink(source, destination)

@cli.command()
@require_elevated_privileges
@pass_state
def stop(state):
    """
    Stop stopping services from starting.

    All services launched via invoke-rc.d will be denied the chance to startup
    once you call start, and they'll continue being denied until you call stop.
    Stop will remove its negative policy enforcer, and will reinstall any
    existing policy enforcer.
    """
    from os.path import join
    from os import remove
    from shutil import move
    original = join(state.home, "policy-rc.d")
    policy = join(state.install_dir, "policy-rc.d")
    sideline = join(state.install_dir, "policy-rc.d.sidelined")
    if not exists(policy):
        echo("Negative policy enforcement has already stopped!")
        exit(0)
    if not are_the_same(original, policy):
        if exists(sideline):
            broken()
            echo("A sideline AND third party policy enforcer exist!")
            echo("Please review both policy enforcers and remove one before calling stop again")
            echo("The current sidelined policy enforcer will be overwritten if you call start")
            exit(1)
        else:
            echo("A third party policy enforcer is already active!")
            exit(1)
    if exists(policy):
        remove(policy)
    if exists(sideline):
        move(sideline, policy)

@cli.command()
@pass_state
def status(state):
    """Determine the status of policy enforcement."""
    from os.path import join
    original = join(state.home, "policy-rc.d")
    policy = join(state.install_dir, "policy-rc.d")
    sideline = join(state.install_dir, "policy-rc.d.sidelined")
    if exists(sideline):
        if not exists(policy):
            broken()
            echo("A sidelined policy enforcer exists, but no active policy enforcer")
            echo("Try moving the sidelined enforcer back into place")
            exit(1)
    if exists(policy):
        if are_the_same(original, policy):
            active()
            echo("Policy enforcement is active")
            exit(0)
        else:
            if exists(sideline):
                broken()
                echo("A sidelined AND third party policy enforcer exist!")
                echo("The current sidelined policy enforcer will be overwritten if you call start")
                exit(1)
            inactive()
            echo("Third party policy enforcement is active")
            exit(0)
    else:
        inactive()
        echo("No policy enforcement is active")


if __name__ == "__main__":
    cli()
