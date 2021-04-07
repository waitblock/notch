# Notch Setup rev 1 <Untested>
# *I cannot test this script properly because I do not have root on the computer I am using.*
# If you can verify that this script works on MacOSX>=10.15.7, please email me.
if command -v python 1>/dev/null 2>&1; then
  echo You already have python installed.
else
  xcode-select --install
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install python
fi
echo Instaling libraries...
python3 -m pip install -r requirements.txt