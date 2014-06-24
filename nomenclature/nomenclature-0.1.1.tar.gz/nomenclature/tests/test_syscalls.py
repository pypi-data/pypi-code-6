"""
Tests for :py:module:`nomenclature.syscalls`.
"""
import os, socket, errno
from unittest import TestCase, skipIf
from subprocess import check_call

from nomenclature.syscalls import unshare, setns, CLONE_NEWUTS

class TestErrors(TestCase):

    @skipIf(os.getuid() == 0, "root doesn't get permission errors.")
    def assert_permission_denied(self, f, *args):
        """
        Calling f` raises OSError with EPERM.
        """
        with self.assertRaises(OSError) as cm:
            f(*args)
        self.assertEqual(cm.exception.errno, errno.EPERM)

    def test_unshare(self):
        """
        When the user is not root, calling unshare fails with EPERM.
        """
        self.assert_permission_denied(unshare, CLONE_NEWUTS)

    def test_setns(self):
        """
        When the user is not root, calling setns fails with EPERM.
        """
        fd = os.open('/proc/self/ns/uts', os.O_RDONLY)
        self.addCleanup(os.close, fd)
        self.assert_permission_denied(setns, fd, CLONE_NEWUTS)

    def test_setns_bad_fd(self):
        """
        When called with an fd that is does not represent a namespace,
        setns fails with EINVAL.
        """
        with self.assertRaises(OSError) as cm:
            setns(0, 0)
        self.assertEqual(cm.exception.errno, errno.EINVAL)


class TestSwitching(TestCase):

    @skipIf(os.getuid() != 0, "Only root can manipulate namespaces.")
    def test_namespaces(self):
        """
        unshare and setns manipulate namespaces.

        unshare(CLONE_NEWUTS) creates a new UTS (hostname) namespace,
        where changes to the hostname don't affect the original hostname.

        setns(fd, CLONE_NEWUTS) switches to the namespace associated to the
        file descriptor.
        """
        # Get the current hostname.
        name = socket.gethostname()
        target_name = name + '.changed'

        # Save the original namespace, and restore it at the end of the test.
        original_namespace = os.open('/proc/self/ns/uts', os.O_RDONLY)
        self.addCleanup(os.close, original_namespace)
        self.addCleanup(setns, original_namespace, CLONE_NEWUTS)

        # Create a new namespace.
        unshare(CLONE_NEWUTS)
        new_namespace = os.open('/proc/self/ns/uts', os.O_RDONLY)
        self.addCleanup(os.close, new_namespace)

        # Set a new hostname in the new namespace.
        check_call(['hostname', target_name])
        self.assertEqual(socket.gethostname(), target_name)

        # Check that the original hostname is still the hostname in the
        # original namespace.
        setns(original_namespace, CLONE_NEWUTS)
        self.assertEqual(socket.gethostname(), name)

        # Check that the new hostname is still the hostname in the new
        # namepsace.
        setns(new_namespace, CLONE_NEWUTS)
        self.assertEqual(socket.gethostname(), target_name)
