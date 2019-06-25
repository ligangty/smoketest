#!/bin/bash

THIS=$(cd ${0%/*} && echo $PWD/${0##*/})
BASEDIR=`dirname ${THIS}`
GITDIR=$BASEDIR/git
INDYDIR=$BASEDIR/indy
AQDIR=$BASEDIR/auditquery

rmIfExists()
{
    target=$1
    echo "Removing $1"
    if [ -d $target ]
    then
        rm -rf $target
    fi
    echo "$1 Removed"
}

rmIfExists $GITDIR
rmIfExists $INDYDIR/pkg
rmIfExists $AQDIR/pkg