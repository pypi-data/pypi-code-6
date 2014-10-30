"""Update commands that are send to the balancer manager.
"""

class UpdateMember(object):
    """A command that updates a single member.
    """
    # pylint: disable = too-few-public-methods
    # pylint: disable = too-many-instance-attributes

    def __init__(self, cluster_name, member):
        """Creates a new update command for a single member.

        :param cluster_name: The name of the member's cluster.
        :param member: the member's current status.
        """
        self.cluster_name = cluster_name
        self.worker_url = member.worker_url
        self.route = member.route
        self.route_redirect = member.route_redirect
        self.load_factor = member.load_factor
        self.lb_set = member.lb_set
        self.ignore_errors = member.ignore_errors
        self.draining_mode = member.draining_mode
        self.enabled = member.enabled
        self.hot_standby = member.hot_standby

    def to_form(self):
        """Create the form parameters for this command.
        """
        return {
            'b': self.cluster_name,
            'w': self.worker_url,
            'w_wr': self.route,
            'w_rr': self.route_redirect,
            'w_lf': self.load_factor,
            'w_ls': self.lb_set,
            'w_status_I': self.ignore_errors,
            'w_status_N': self.draining_mode,
            'w_status_D': not self.enabled,
            'w_status_H': self.hot_standby
        }
