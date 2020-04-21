import clara.plugins.clara_p2p as clara_p2p
from clara.utils import get_from_config
from configparser import ConfigParser
import os

def fake_config():
    config = ConfigParser()
    config.read('example-conf/config.ini')
    return config



def fakechmod(file, mode):

    os.chmod(file, mode)

def test_mktorrent(mocker, tmpdir_factory):

    fn = tmpdir_factory.mktemp("torrent")
    torrent_dir = str(fn)
    seed_file = os.path.join(torrent_dir,'file1.torrent')
    open(seed_file,'a')

    def fake_getfromconfig(section, value, dist=''):
        if section == "p2p" and value == "seeders":
            return "seeders1,seeders2:{}".format(seed_file)
        if section == "images" and value == "trg_dir":
            return torrent_dir

        return get_from_config(section, value, dist)

    mocker.patch("clara.utils.getconfig", side_effect=fake_config)
    mocker.patch("clara.plugins.clara_p2p.get_from_config", side_effect=fake_getfromconfig)
    mocker.patch("clara.plugins.clara_p2p.os.path.isfile")
    mocker.patch("clara.plugins.clara_p2p.os.path.isfile")
    mocker.patch("clara.plugins.clara_p2p.os.remove")
    mocker.patch("clara.plugins.clara_p2p.os.chmod")
    m_run = mocker.patch("clara.plugins.clara_p2p.run")
    clara_p2p._opts['dist'] ='calibre9'

    clara_p2p.mktorrent(None)

    m_run.assert_called_with(["/usr/bin/mktorrent", "-a",
                              "http://server2:6881/announce", '-o',
                              u'/srv/clara/website/boot/file2.torrent',
                              u'/srv/clara/website/boot/calibre9.squashfs'])
    file_permisions = os.stat(seed_file)
    assert file_permisions.st_mode == 33188#'0100644'
    file_permisions = os.stat(torrent_dir)
    assert file_permisions.st_mode == 16877#'040755'