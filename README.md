sudo date -s "Sept 8 12:31"

sudo apt-get update



sudo apt-get install libjpeg62-turbo-dev

sudo apt-get install cmake

git clone https://github.com/jacksonliam/mjpg-streamer.git 

cd ~/mjpg-streamer/mjpg-streamer-experimental

sudo make clean all


sudo rm -rf /opt/mjpg-streamer

sudo mv ~/mjpg-streamer/mjpg-streamer-experimental /opt/mjpg-streamer

sudo rm -rf ~/mjpg-streamer

LD_LIBRARY_PATH=/opt/mjpg-streamer/ /opt/mjpg-streamer/mjpg_streamer -i "input_raspicam.so -fps 15 -q 50 -x 840 -y 640" -o "output_http.so -p 9000 -w /opt/mjpg-streamer/www" &








Section 





---------- Section F ---------------
{'852DB520\r\n': 'F23', '86E90422\r\n': 'F10', '76759824\r\n': 'F43', '765E3024\r\n': 'F45', '75366520\r\n': 'F33', 'F4F68E23\r\n': 'F51', '8563E120\r\n': 'F30', '66FD5124\r\n': 'F52', '8065682B\r\n': 'F65', 'B5F7BD22\r\n': 'F58', 'B58C4522\r\n': 'F64', '75B56520\r\n': 'F20', '642B8B24\r\n': 'F40', 'B5655F22\r\n': 'F63', '8601DE24\r\n': 'F42', '76CC0924\r\n': 'F49', '8698EF22\r\n': 'F29', 'E4CCA923\r\n': 'F57', '86EF6522\r\n': 'F2', '86E52522\r\n': 'F9', 'F48DC823\r\n': 'F54','8024112B\r\n': 'F69', 'F4476023\r\n': 'F48', '756BF020\r\n': 'F5', '86E6E422\r\n': 'F17', '75AEA920\r\n': 'F25', '803E7E2B\r\n': 'F68', '66FCDA24\r\n': 'F39', '860D2224\r\n': 'F36', '86153622\r\n': 'F14', '66668324\r\n': 'F35', '75125420\r\n': 'F19', '7519E420\r\n': 'F24', '8637F822\r\n': 'F22', 'B51E7022\r\n': 'F61', '86471622\r\n': 'F28', '75753E20\r\n': 'F15', '6688A824\r\n': 'F46', '7519E620\r\n': 'F16', 'F4C7E123\r\n': 'F62', '858BAA20\r\n': 'F26', '62E9C92E\r\n': 'F53', '8591B720\r\n': 'F11', '76B45122\r\n': 'F4', '75705B20\r\n': 'F31', '762A6D24\r\n': 'F50', '86043E22\r\n': 'F27', 'B55D2C22\r\n': 'F67', '549EDC24\r\n': 'F41', '66935424\r\n': 'F37', '72819B2E\r\n': 'F66', '86924B22\r\n': 'F13', '755F4320\r\n': 'F8', '76C03B24\r\n': 'F47', '85A99320\r\n': 'F21', '7569E620\r\n': 'F1', '854D6420\r\n': 'F3', '8663DF22\r\n': 'F32', 'F4C68623\r\n': 'F56', '75173420\r\n': 'F7', '52A29A2E\r\n': 'F60', '8287CC2E\r\n': 'F70', '62DA042E\r\n': 'F55', '54303824\r\n': 'F38', '66B13F24\r\n': 'F44', '50D6632B\r\n': 'F59', '8515E220\r\n': 'F12', '76ED0B22\r\n': 'F6', '66869624\r\n': 'F34', '755FFF20\r\n': 'F18', '7269282E\r\n': 'F71'}




Left_beds = ['F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F54', 'F55', 'F56', 'F57', 'F58', 'F59', 'F66', 'F67', 'F68', 'F69', 'F70', 'F71']