#! /bin/bash
tarsnap cf Documents-`date +%F` --cachedir /root/.tarsnap_cache --keyfile /root/tarsnap.key ~/Documents
