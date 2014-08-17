# Copyright (c) 2012, Wide Open Technologies. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer. Redistributions in
# binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution. THIS SOFTWARE IS
# PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import shutil
import subprocess
import sys
import time
import zipfile

import logging

def get_shared_files_dir():
    root_dir = None
    if sys.platform.startswith("win"):
        root_dir = os.environ["ALLUSERSPROFILE"]
    elif sys.platform.startswith("darwin"):
        root_dir = "/Users/Shared"
    shared_dir = os.path.join(root_dir, "goodasnew")
    if not os.path.exists(shared_dir):
        os.makedirs(shared_dir)
    return shared_dir

log_dir = get_shared_files_dir()
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    os.chmod(log_dir, 0777)
    
log_file = os.path.join(log_dir, "goodasnew.log")
filename = None
if not os.path.exists(log_file) or os.access(log_file, os.W_OK):
    filename = log_file

logging.basicConfig(filename=filename, filemode='w', level=logging.INFO)
log = logging.getLogger()

def main(pid, filename, dest_dir, temp_dir, exe_name):
    timeout = 120
    wait_time = 0
    still_alive = True
    while still_alive:
        # query for process information, if we don't see the process id in the output
        # that means the process has completed
        output = ''
        if sys.platform.startswith('win'):
            output = subprocess.Popen(['tasklist', '/fi', 'PID eq %s' % pid], stdout=subprocess.PIPE).stdout.read()
        else:
            output = subprocess.Popen(['ps', '-p', pid], stdout=subprocess.PIPE).stdout.read()
        
        if output.find(pid) != -1:
            time.sleep(1)
            wait_time += 1
        else:
            break
    
    logging.info("Parent process finished after waiting %d seconds" % wait_time)
    
    # try to do an installation, and rollback if we fail for some reason partway in.
    backup_dir = os.path.join(temp_dir, "backup")
    basename = dest_dir.split(os.sep)[-1]
    parent_dir = os.path.dirname(dest_dir)
    succeeded = False
    try:
        extract_dir = os.path.join(temp_dir, "zip_contents")
        # on Unix, we lose file permissions if we use Python's built in zip
        # functionality, so only use it under Win.
        logging.info("Extracting package archive...")
        if sys.platform.startswith('win'):
            zip = zipfile.ZipFile(os.path.join(temp_dir, filename), 'r')
            zip.extractall(extract_dir)
            zip.close()
        else:
            os.system("unzip -d %s %s" % (extract_dir, os.path.join(temp_dir, filename).replace(" ", "\\ ")))
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        logging.info("Backing up existing application files...")
        shutil.copytree(dest_dir, backup_dir)
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir, ignore_errors=True)
        root = os.path.join(extract_dir, basename)
        logging.info("Installing update...")
        if sys.platform.startswith('win'):
            root = extract_dir

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for afile in os.listdir(root):
                fullpath = os.path.join(root, afile)
                if os.path.isfile(fullpath):
                    shutil.copy(fullpath, os.path.join(dest_dir, afile))
                else:
                    shutil.copytree(fullpath, os.path.join(dest_dir, afile))
        else:
            shutil.move(root, dest_dir)
        logging.info("Files installed successfully.")
        succeeded = True
    except Exception, e:
        import traceback
        logging.error("Error installing files")
        logging.error(traceback.format_exc(e))
        backup_app_dir = os.path.join(backup_dir, basename)
        logging.info("Restoring from backup...")
        if os.path.exists(backup_app_dir):
            try:
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                shutil.copytree(backup_app_dir, dest_dir)
            except Exception, e:
                logging.error("Error restoring from backup. Error details:")
                logging.error(traceback.format_exc(e))
    
    logging.info("Removing temp directory...")
    shutil.rmtree(temp_dir, ignore_errors=True)
    if succeeded:
        logging.info("Starting application...")
        if sys.platform.startswith('darwin'):
            os.system('open -a %s' % dest_dir.replace(" ", "\\ "))
        else:
            os.startfile('%s\\%s' % (dest_dir, exe_name))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
