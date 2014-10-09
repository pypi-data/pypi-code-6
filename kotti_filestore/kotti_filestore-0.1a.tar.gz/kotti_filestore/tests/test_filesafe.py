import os
import transaction
from pytest import raises


def test_split():
    """ Test Cases for kotti_filestore.split_by_n(). """

    import kotti_filestore
    teststring = "ABCDEF"
    teststring2 = teststring
    # split_by_n() without second parameter should split the string by 2
    for substring in kotti_filestore.split_by_n(teststring):
        assert substring == teststring[:2]
        teststring = teststring[2:]
    # Testing splitting up by a length of 3
    for substring in kotti_filestore.split_by_n(teststring2, 3):
        assert substring == teststring2[:3]
        teststring2 = teststring2[3:]


def test_path(filestore):
    """ Test Cases for filestore.path(). """

    addedstring = "ABCDEF"
    # Test that path() returns the filepath by splitting up addedstring and
    # adding the new path to the initpath
    assert filestore.path(addedstring) == "/tmp/kotti_filestore/AB/CD/EF"
    # Without any parameter path() should just add /tmp to the initpath
    assert filestore.path() == "/tmp/kotti_filestore/tmp"


def test_create_directory(tmpdir):
    """ Test Cases for kotti_filestore.create_directory(). """

    import kotti_filestore

    os.makedirs("/tmp/kotti_filestore/test/")
    # Test that function returns without exception if directory already exists
    kotti_filestore.create_directory("/tmp/kotti_filestore/test")
    # Test that new directory is created if specified directory does not exist
    kotti_filestore.create_directory("/tmp/kotti_filestore/test2")
    assert os.path.isdir("/tmp/kotti_filestore/test2")


def test_read(tmpdir, request, filestore):
    """ Test Cases for filestore.read(). """

    testtext = "Testtext\n"
    os.makedirs("/tmp/kotti_filestore/te")
    testfile = open("/tmp/kotti_filestore/te/st", "w")
    # Write into testfile then give id to read() and test that
    # return value equals the value written into file
    testfile.write(testtext)
    testfile.close()
    assert filestore.read("test") == testtext


def test_remove_base_directory(tmpdir, filestore):
    """ Test Cases for filestore.remove_base_directory(). """

    os.makedirs("/tmp/kotti_filestore/te/st/di/re/ct/or/y")
    # Add random content to directory te
    os.makedirs("/tmp/kotti_filestore/te/directorycontent")
    # Test that function returns without exception when path is
    # filestore directory
    filestore.remove_base_directory("/tmp/kotti_filestore/")
    filestore.remove_base_directory("/tmp/kotti_filestore/te/st/di/re/ct/or/y")
    # Test that all empty directorys have been removed
    assert os.path.isdir("/tmp/kotti_filestore/te/st") is False
    # Test that recursive removal has stopped at non-empty directory
    assert os.path.isdir("/tmp/kotti_filestore/te")


def test_delete(transactionmockup, tmpdir, filestore):
    """ Test Cases for filestore.remove_base_directory(). """

    os.makedirs("/tmp/kotti_filestore/te")
    testfile = open("/tmp/kotti_filestore/te/st", "w")
    testfile.write("test")
    testfile.close()
    filestore.delete("test")
    # Check that file no longer exists
    assert os.path.isfile("/tmp/kotti_filestore/te/st") is False
    # Check that containing directory no longer exists
    assert os.path.isdir("/tmp/kotti_filestore/te") is False
    # Check that initial directory has not been deleted
    assert os.path.isdir("/tmp/kotti_filestore")


def test_write(db_session, tmpdir, filestore):
    """ Test Cases for filestore.write(). """

    testfile_id = filestore.write("test")
    # Test that file does not exist before the commit
    with raises(IOError):
        testfile = open(filestore.path(testfile_id), "r")
    transaction.commit()
    # Test that after committing, file exists and contains correct data
    testfile = open(filestore.path(testfile_id), "r")
    assert testfile.read() == "test"
    testfile.close()
