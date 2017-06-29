echo travis_fold:start:TestInstallation
echo "Test installation"
python --version
python -c "import openpathsampling"
python -c "import pyretis"
echo travis_fold:end:TestInstallation
