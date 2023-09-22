#! /bin/bash
# To install Latin Modern fonts on your user space, run "source install_latin_modern_fonts.sh" in a terminal
STARTING_POINT=$PWD
mkdir -p ~/.fonts
cd ~/.fonts
# Install Latin Modern Math
wget http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf
# Install Latin Modern Roman
wget https://www.1001fonts.com/download/latin-modern-roman.zip
unzip latin-modern-roman.zip -d latin-modern-roman
rm -f latin-modern-roman.zip
# Install Latin Modern Sans
unzip file.zip -d destination_folder
wget https://www.1001fonts.com/download/latin-modern-sans.zip
unzip latin-modern-sans.zip -d latin-modern-sans
rm -f latin-modern-sans.zip
# Return to starting folder
cd $STARTING_POINT
# Clear matplotlib cache
rm -rf ~/.cache/matplotlib
