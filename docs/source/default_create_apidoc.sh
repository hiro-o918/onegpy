mv reference/index.rst ./index.rst.bk
rm -r reference
rm -r ../build/*
pushd ../../
python docs/source/create_apidoc.py -f -e -M -m -T -o docs/source/reference/ onegpy
popd
mv index.rst.bk reference/index.rst
rm reference/.rst
pushd ../
make html
popd