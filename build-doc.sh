#!/usr/bin/env sh

BUILDPATH=docs
SOURCEPATH=docs-rst-sources

rm -rf $BUILDPATH/_static/*
rm -rf $BUILDPATH/_sources/*
rm -rf $BUILDPATH/_images/*
rm -rf $BUILDPATH/*.html
rm -rf $BUILDPATH/*.js

touch $BUILDPATH/.nojekyll
sphinx-build -b html $SOURCEPATH $BUILDPATH
echo 'Documentation website in '$BUILDPATH
