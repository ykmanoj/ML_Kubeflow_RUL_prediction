#!/bin/sh

echo "\nBuild and push data component"
./data/build_image.sh

echo "\nBuild and push preprocess component"
./preprocess/build_image.sh

echo "\nBuild and push linear regression component"
./lr/build_image.sh

echo "\nBuild and push random forest component"
./rf/build_image.sh