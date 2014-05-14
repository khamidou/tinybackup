#! /bin/bash
tarsnap cvf Documents-`date +%F` --cachedir /root/.tarsnap_cache --keyfile /root/tarsnap.key --exclude Documents/Livres --exclude Documents/isos/ --exclude Documents/Cours ~/Documents
