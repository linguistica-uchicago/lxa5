#!/usr/bin/env sh

BUILDPATH=../lxa5-gh-pages
SOURCEPATH=doc

if [ -d "$BUILDPATH" ]; then
  rm -rf $BUILDPATH/*
else
  mkdir $BUILDPATH
fi

touch $BUILDPATH/.nojekyll
sphinx-build -b html $SOURCEPATH $BUILDPATH
echo 'Doc HTML files in '$BUILDPATH
