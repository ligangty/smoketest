#!/bin/bash

THIS=$(cd ${0%/*} && echo $PWD/${0##*/})
BASEDIR=`dirname ${THIS}`
GITDIR=$BASEDIR/git
INDYDIR=$BASEDIR/indy
AQDIR=$BASEDIR/auditquery

rm -rf $INDYDIR/pkg && mkdir -p $INDYDIR/pkg
rm -rf $AQDIR/pkg && mkdir -p $AQDIR/pkg
mkdir -p $GITDIR

prepare() 
{
    repo=$1
    src_tar=$2
    dest_tar=$3
    if [ ! -f $GITDIR/$repo/pom.xml ];
    then
        git clone https://github.com/ligangty/$repo.git $GITDIR/$repo
    fi
    cd $GITDIR/$repo
    git fetch origin 
    git checkout changelog
    git reset --hard origin/changelog
    mvn clean install -DskipTests
    cp $src_tar $dest_tar    
}

prepare indy $GITDIR/indy/deployments/launcher/target/indy-launcher-*-complete.tar.gz $INDYDIR/pkg/indy.tar.gz
prepare auditquery $GITDIR/auditquery/deployments/standalone-rest/target/auditquery-standalone-rest-*.tar.gz $AQDIR/pkg/auditquery.tar.gz

docker-compose up
