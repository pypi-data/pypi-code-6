class CouchbaseCluster(object):
    def __init__(self, connstr, admin_user=None, admin_password=None):
        """
        Create a new cluster object. A cluster object represents a
        Couchbase Cluster. You may retrieve information about the cluster and
        create new :class:`Bucket` objects as well

        :param string connstr: A connection string indicating how to connect
        to the cluster.
        :param string admin_user: The administrative username
        :param string admin_password: The administrative password
        """
        self.connstr = connstr
        self.admin_user = admin_user
        self.admin_password = admin_password

    def open_bucket(self, name, bucket_password=None, connstr=None):
        """
        Create a new connection to a couchbase bucket. The bucket is used
        for accessing documents in the cluster.

        :param string name: The name of the bucket to accesss
        :param string bucket_password: The password for the bucket (if required)
        """
        if connstr is None:
            connstr = self.connstr

    def open_admin(self, admin_user=None, admin_password=None):
        pass
