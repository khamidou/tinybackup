# fabfile for update and deploy
# it's necessary to specify an host
from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import upload_template

PACKAGES = ('build-essential')
TARSNAP_VERSION = '1.0.35'

def setup_packages():
    sudo("apt-get update")
    for package in PACKAGES:
        sudo('apt-get -y install %s' % package)

def build_tarsnap():
    #FIXME: validate keys
    local("curl 'https://www.tarsnap.com/download/tarsnap-autoconf-%s.tgz' -o /tmp/tarsnap.tgz" % TARSNAP_VERSION)
    #local("curl 'https://www.tarsnap.com/download/tarsnap-sigs-1.0.35.asc' -o /tmp/")
    #local("curl 'https://www.tarsnap.com/tarsnap-signing-key-2013.asc' -o /tmp/")
    #local("gpg --decrypt /tmp/tarsnap-sigs-1.0.35.asc")
    with lcd('/tmp'):
        local("tar xzvf tarsnap.tgz")
        with lcd('/tmp/tarsnap-autoconf-%s' % TARSNAP_VERSION):
            local('./configure && make')
            local('sudo make install')

def register_machine():
    email = raw_input("Tarsnap email: ").rstrip()
    mname = raw_input("Machine name: ").rstrip()
    local("sudo tarsnap-keygen --keyfile /root/tarsnap.key --user %s --machine %s" % (email, mname))
    print "Saved Tarsnap key to /root/tarsnap.key. MAKE A COPY SOMEWHERE SAFE."

def setup_cron_job():
    local("sudo cp tarsnap-backup.sh /etc/cron.daily") 
    print "Saved CRON script to /etc/cron.daily. Edit /etc/cron.daily/tarsnap-backup.sh if you want to add directories to the backup."

def setup():
    setup_packages()
    build_tarsnap()
    raw_input("If it's not done, go create an account at http://tarsnap.com, and add some balance to your account.")
    register_machine()
    setup_cron_job()
