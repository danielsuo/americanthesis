#!/usr/bin/env/bash

BASE_URL="https://suo.seas.harvard.edu/files/suo/files"

for id in {7..483}
do
  wget $BASE_URL/$id.pdf
done
