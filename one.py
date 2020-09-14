import tornado.ioloop
import tornado.web
import datetime
import gpiozero
import time
import serial
import RPi.GPIO as GPIO
import os
import fetch_data


robot = gpiozero.Robot(left=(11,25), right=(9,10))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT) #temperature
GPIO.setup(5,GPIO.OUT) #pressure
GPIO.setup(26,GPIO.OUT) #spo2

GPIO.output(5,1)
GPIO.output(6,1)
GPIO.output(26,1)


rfid_dict = {'7557FC20\r\n': 'D18', '9618BB22\r\n': 'D39', '75F4B220\r\n': 'D11', '8630D222\r\n': 'D62', '864FD722\r\n': 'D63', '857B2220\r\n': 'D76', '7564B620\r\n': 'D33', '75859320\r\n': 'D87', '75BBAD20\r\n': 'D1', '8656E322\r\n': 'D43', '759B1E20\r\n': 'D96', '850ECC20\r\n': 'D40', '75E02E20\r\n': 'D6', '8592D520\r\n': 'D98', '86270022\r\n': 'D23', '963B4422\r\n': 'D3', '853B1220\r\n': 'D30', '86931A22\r\n': 'D24', '8685C422\r\n': 'D4', '756D6020\r\n': 'D97', '76B23C22\r\n': 'D45', '7519CC20\r\n': 'D89', '76D7A222\r\n': 'D56', '85679120\r\n': 'D91','759F2120\r\n': 'D49', '8574BF20\r\n': 'D31', '86D64022\r\n': 'D27', '8538E320\r\n': 'D84', '75988620\r\n': 'D74', '7589BB20\r\n': 'D60', '86D15522\r\n': 'D25', '860CCA22\r\n': 'D51', '850D3920\r\n': 'D58', '96578622\r\n': 'D92', '9650EF22\r\n': 'D22', '8534F920\r\n': 'D7', '855CA420\r\n': 'D29', '85130220\r\n': 'D48', '75933D20\r\n': 'D75', '86E76922\r\n': 'D36', '86CCA622\r\n': 'D19', '75E17920\r\n': 'D17', '86221222\r\n': 'D83', '75A1DC20\r\n': 'D93', '7578DC20\r\n': 'D2', '75F9A620\r\n': 'D32', '85E8A420\r\n': 'D20', '701B8A2B\r\n': 'D67', '759DD720\r\n': 'D28', '9629E522\r\n': 'D70', '75719620\r\n': 'D38', '756F1120\r\n': 'D8', '7599A020\r\n': 'D64', '85B2E620\r\n': 'D73', '757B0520\r\n': 'D52', '757ED820\r\n': 'D15', '85221A20\r\n': 'D57', '7576BC20\r\n': 'D72', '86E66822\r\n': 'D86', '859E1420\r\n': 'D47', '8555B320\r\n': 'D90', '8658B822\r\n': 'D34', '96335822\r\n': 'D35', '86F25022\r\n': 'D42', '757BA820\r\n': 'D10', '75CC2720\r\n': 'D13', '859A6D20\r\n': 'D94', '96026C22\r\n': 'D26', '8501A820\r\n': 'D50', '85307E20\r\n': 'D54', '850AEA20\r\n': 'D53', '86081E22\r\n': 'D5', '86375D22\r\n': 'D55', '86E9D022\r\n': 'D12', '852AB720\r\n': 'D88', '8676A522\r\n': 'D95', '755D5620\r\n': 'D65', '7581F020\r\n': 'D9', '75123620\r\n': 'D14', '7573DC20\r\n': 'D21', '96127C22\r\n': 'D79', '86323822\r\n': 'D61', '86A72B22\r\n': 'D59', '86068A22\r\n': 'D82', '7594B820\r\n': 'D80', '851E8320\r\n': 'D46', '755AAC20\r\n': 'D37', '76D17522\r\n': 'D16', '76ADC822\r\n': 'D66', '96054322\r\n': 'D41', '96191F22\r\n': 'D78', '8637DE22\r\n': 'D81', '606F782B\r\n': 'D68', 'A5D5C622\r\n': 'D69', '86EEA922\r\n': 'D71', '963D8522\r\n': 'D77', '8577BF20\r\n': 'D44', '86B79622\r\n': 'D85', '86EAF922\r\n': 'C47', '751F1120\r\n': 'C5', '75C27820\r\n': 'C8', '859C6120\r\n': 'C65', '75507F20\r\n': 'C59', '76353724\r\n': 'C21', '86257922\r\n': 'C34', '76B67222\r\n': 'C29', '66CB9524\r\n': 'C22', '96533322\r\n': 'C50', '8577D620\r\n': 'C58', '75847F20\r\n': 'C64', '8546FD20\r\n': 'C4', '767A4724\r\n': 'C24', '85159720\r\n': 'C57', '86BAFD22\r\n': 'C2', '858A0320\r\n': 'C32', '8504A820\r\n': 'C31', '757BA620\r\n': 'C35', '7586DF20\r\n': 'C56', '75AA0720\r\n': 'C3', '85B27D20\r\n': 'C38', '962C5922\r\n': 'C53', '85430420\r\n': 'C17', '86DD7822\r\n': 'C41', '753AF620\r\n': 'C6', '75F5F220\r\n': 'C9', '9623AD22\r\n': 'C46', '855BCB20\r\n': 'C39', '75C5D520\r\n': 'C42', '8676F722\r\n': 'C1', '8666DE22\r\n': 'C40', '85838F20\r\n': 'C60', '75172B20\r\n': 'C10', '8591E120\r\n': 'C45', '75B91320\r\n': 'C51', '76743A24\r\n': 'C23', '75F79320\r\n': 'C16', '7564E520\r\n': 'C27', '755AD520\r\n': 'C26', '85971B20\r\n': 'C66', '76F73022\r\n': 'C7', '75EEA420\r\n': 'C25', '85839620\r\n': 'C48', '757EBC20\r\n': 'C52', '8548EF20\r\n': 'C18', '960E0122\r\n': 'C49', '75ABA620\r\n': 'C19', '86FD7122\r\n': 'C36', '867DC122\r\n': 'C28', '8552FE20\r\n': 'C62', '8556A120\r\n': 'C15', '665FA624\r\n': 'C20', '754D2220\r\n': 'C54', '75AB3420\r\n': 'C44', '75A1F220\r\n': 'C43', '76F21722\r\n': 'C11', '868D1822\r\n': 'C13', '75942320\r\n': 'C14', '86E8FB22\r\n': 'C55', '75A9AD20\r\n': 'C12', '756B0F20\r\n': 'C37', '759B0D20\r\n': 'C30', '851C0020\r\n': 'C63', '8561A620\r\n': 'C33', '75817520\r\n': 'C61', '852DB520\r\n': 'F23', '86E90422\r\n': 'F10', '76759824\r\n': 'F43', '765E3024\r\n': 'F45', '75366520\r\n': 'F33', 'F4F68E23\r\n': 'F51', '8563E120\r\n': 'F30', '66FD5124\r\n': 'F52', '8065682B\r\n': 'F65', 'B5F7BD22\r\n': 'F58', 'B58C4522\r\n': 'F64', '75B56520\r\n': 'F20', '642B8B24\r\n': 'F40', 'B5655F22\r\n': 'F63', '8601DE24\r\n': 'F42', '76CC0924\r\n': 'F49', '8698EF22\r\n': 'F29', 'E4CCA923\r\n': 'F57', '86EF6522\r\n': 'F2', '86E52522\r\n': 'F9', 'F48DC823\r\n': 'F54','8024112B\r\n': 'F69', 'F4476023\r\n': 'F48', '756BF020\r\n': 'F5', '86E6E422\r\n': 'F17', '75AEA920\r\n': 'F25', '803E7E2B\r\n': 'F68', '66FCDA24\r\n': 'F39', '860D2224\r\n': 'F36', '86153622\r\n': 'F14', '66668324\r\n': 'F35', '75125420\r\n': 'F19', '7519E420\r\n': 'F24', '8637F822\r\n': 'F22', 'B51E7022\r\n': 'F61', '86471622\r\n': 'F28', '75753E20\r\n': 'F15', '6688A824\r\n': 'F46', '7519E620\r\n': 'F16', 'F4C7E123\r\n': 'F62', '858BAA20\r\n': 'F26', '62E9C92E\r\n': 'F53', '8591B720\r\n': 'F11', '76B45122\r\n': 'F4', '75705B20\r\n': 'F31', '762A6D24\r\n': 'F50', '86043E22\r\n': 'F27', 'B55D2C22\r\n': 'F67', '549EDC24\r\n': 'F41', '66935424\r\n': 'F37', '72819B2E\r\n': 'F66', '86924B22\r\n': 'F13', '755F4320\r\n': 'F8', '76C03B24\r\n': 'F47', '85A99320\r\n': 'F21', '7569E620\r\n': 'F1', '854D6420\r\n': 'F3', '8663DF22\r\n': 'F32', 'F4C68623\r\n': 'F56', '75173420\r\n': 'F7', '52A29A2E\r\n': 'F60', '8287CC2E\r\n': 'F70', '62DA042E\r\n': 'F55', '54303824\r\n': 'F38', '66B13F24\r\n': 'F44', '50D6632B\r\n': 'F59', '8515E220\r\n': 'F12', '76ED0B22\r\n': 'F6', '66869624\r\n': 'F34', '755FFF20\r\n': 'F18', '7269282E\r\n': 'F71', '6692B624\r\n': 'E67', '76C90024\r\n': 'E29', 'D4C8D5CE\r\n': 'E82', '6230532E\r\n': 'E14', 'B2CD412E\r\n': 'E25', '\n': 'E65', '7041102B\r\n': 'E41', '841FBFCE\r\n': 'E84', 'A5A24222\r\n': 'E89', '92A3EC2E\r\n': 'E40', '6274082E\r\n': 'E12', '623DE02E\r\n': 'E17', 'A275732E\r\n': 'E43', '76094A24\r\n': 'E68', '54613124\r\n': 'E36', '66F95F24\r\n': 'E11', '623BE42E\r\n': 'E95', '52B8152E\r\n': 'E75', 'B5D6BF22\r\n': 'E6', '6285972E\r\n': 'E74', 'F4DFAF23\r\n': 'E52', '62ED522E\r\n': 'E96', '765CE624\r\n': 'E56', 'A2D9812E\r\n': 'E30', '86181824\r\n': 'E81', 'F4529423\r\n': 'E54', 'B28F842E\r\n': 'E26', '52D7D62E\r\n': 'E76', '763D3224\r\n': 'E60', '6668EB24\r\n': 'E16', 'C247612E\r\n': 'E34', '829D6A2E\r\n': 'E103', '7276A02E\r\n': 'E105', '54BEE024\r\n': 'E37', '66E7ED24\r\n': 'E58', '66828824\r\n': 'E64', '62753F2E\r\n': 'E21', '52A9A52E\r\n': 'E100', '6207E32E\r\n': 'E94', 'B4F8C0CE\r\n': 'E83', '768D6324\r\n': 'E63', 'E44EE723\r\n': 'E88', '52E9C02E\r\n': 'E13', 'D4BFD9CE\r\n': 'E91', 'E4C3EF23\r\n': 'E55', '6240412E\r\n': 'E18', '96410124\r\n': 'E77', '96C89124\r\n': 'E79', '66D2B524\r\n': 'E70', '62A41F2E\r\n': 'E99', 'E4AF9823\r\n': 'E59', '66855324\r\n': 'E46', 'F488B323\r\n': 'E53', '76EB9B24\r\n': 'E33', '6663D324\r\n': 'E42', '76F0EC24\r\n': 'E9', '66E72824\r\n': 'E31', '66FFC424\r\n': 'E8', '52A1822E\r\n': 'E72', '60A13B2B\r\n': 'E7', '60CBE62B\r\n': 'E5', '620B3A2E\r\n': 'E20', '62EA802E\r\n': 'E97', '66727B24\r\n': 'E1', '824F0B2E\r\n': 'E102', 'A2FE8B2E\r\n': 'E32', '96252624\r\n': 'E80', '66AA2924\r\n': 'E66', '529EC02E\r\n': 'E101', '8262312E\r\n': 'E2', 'A2F4752E\r\n': 'E38', '66E4F424\r\n': 'E27', '76B98924\r\n': 'E24', '52B5542E\r\n': 'E19', '72C6362E\r\n': 'E104', '964D3024\r\n': 'E78', '76DC0724\r\n': 'E35', 'B501C922\r\n': 'E3', '66FB5B24\r\n': 'E61', 'B5D6AB22\r\n': 'E90', '6233372E\r\n': 'E73', '76E2E924\r\n': 'E39', '626FFE2E\r\n': 'E93', '860C1324\r\n': 'E23', '76CC3D24\r\n': 'E10', '540FC1CE\r\n': 'E85', '62A1DA2E\r\n': 'E98', '669EFD24\r\n': 'E57', '66E8A324\r\n': 'E28', '76578124\r\n': 'E50', 'B21BEB2E\r\n': 'E22', '86006B24\r\n': 'E69', '76CC1F24\r\n': 'E62', '76496324\r\n': 'E48', '627F712E\r\n': 'E86', '66B7E324\r\n': 'E45', '76A08F24\r\n': 'E47', 'B205DC2E\r\n': 'E71', '60AC4C2B\r\n': 'E4', '62FFA02E\r\n': 'E92', '6699BE24\r\n': 'E51', '6660EA24\r\n': 'E44', '76436A24\r\n': 'E49', '8289A82E\r\n': 'E106', 'C21C842E\r\n': 'E15', '76D85C24\r\n': 'E87', 'B5FD5522\r\n': 'G22', '601D5B2B\r\n': 'G36', '60888F2B\r\n': 'G25', 'B5F8BF22\r\n': 'G30', '50CB3E2B\r\n': 'G24', '622A372E\r\n': 'G12', '86A77024\r\n': 'G31', '722C412E\r\n': 'G10', '76E11024\r\n': 'G27', '76964324\r\n': 'G21', '76EA9E24\r\n': 'G20', 'A5C2F722\r\n': 'G33', '7005232B\r\n': 'G28', 'E4EEB223\r\n': 'G32', '86FBE624\r\n': 'G39', '86F3FC24\r\n': 'G35', 'C2116C2E\r\n': 'G14', '76EF1224\r\n': 'G5', '86C0E024\r\n': 'G1', 'B299702E\r\n': 'G40', 'C208C42E\r\n': 'G41', '765B1424\r\n': 'G42', '76A7C124\r\n': 'G29', '961F3024\r\n': 'G2', 'B2B9212E\r\n': 'G44', '50B5992B\r\n': 'G18', '867FCD24\r\n': 'G47', 'A2B8A22E\r\n': 'G45', 'C251B02E\r\n': 'G17', 'A2E63A2E\r\n': 'G3', 'A57E5722\r\n': 'G37', '86BCA224\r\n': 'G46', '969E6D24\r\n': 'G13', '96618524\r\n': 'G6', '66C71B24\r\n': 'G11', '76775624\r\n': 'G8', '764DF524\r\n': 'G38', '6664A324\r\n': 'G15', '868B1224\r\n': 'G9', 'B2F2782E\r\n': 'G19', '767D4F24\r\n': 'G34', 'B217B52E\r\n': 'G7', '760EC624\r\n': 'G4', '860C5524\r\n': 'G16', 'A56B7922\r\n': 'G23', '66C7BC24\r\n': 'G26', 'A20D1B2E\r\n': 'G43', 'F4E99E23\r\n': 'H57', '76FCC524\r\n': 'H55', '961B7824\r\n': 'H42', '6242CB2E\r\n': 'H48', 'F4BADE23\r\n': 'H20', '6218E12E\r\n': 'H46', '828CC02E\r\n': 'H32', '76F51724\r\n': 'H62', '545C3824\r\n': 'H61', '9600BD24\r\n': 'H45', 'D46A6E23\r\n': 'H67', 'D4E2A123\r\n': 'H2', 'F4F00623\r\n': 'H6', '86D58724\r\n': 'H35', '9645ED24\r\n': 'H38', 'F4646723\r\n': 'H58', '72819A2E\r\n': 'H59', '76854524\r\n': 'H63', '7296C02E\r\n': 'H31', '52B4582E\r\n': 'H49', '72353F2E\r\n': 'H34', 'D4776823\r\n': 'H65', 'E47F4823\r\n': 'H21', 'E4AEC423\r\n': 'H19', 'B5656F22\r\n': 'H29', 'D4C81423\r\n': 'H66', '8224ED2E\r\n': 'H56', 'E4B4C523\r\n': 'H22', 'D4A6E523\r\n': 'H9', 'A59B4722\r\n': 'H16', '8220222E\r\n': 'H28', 'B51D3722\r\n': 'H13', '667A5724\r\n': 'H54', 'F484FD23\r\n': 'H25', 'D4CDBA23\r\n': 'H8', 'B565FA22\r\n': 'H15', 'D4C3F923\r\n': 'H1', '86E0EF24\r\n': 'H44', 'F4D82123\r\n': 'H40', 'D4A1AC23\r\n': 'H5', 'C4A4BA23\r\n': 'H7', '860CAC24\r\n': 'H69', 'D46D6623\r\n': 'H4', '862B0424\r\n': 'H33', 'C4EF5923\r\n': 'H24', '8211102E\r\n': 'H30', 'E4A79623\r\n': 'H18', 'B55E6F22\r\n': 'H14', 'C49F8B23\r\n': 'H68', '768B3C24\r\n': 'H51', 'A5612322\r\n': 'H11', '626B532E\r\n': 'H10', '72140B2E\r\n': 'H47', 'F46E0F23\r\n': 'H23', '86E9CD24\r\n': 'H39', '86227424\r\n': 'H43', '6016E42B\r\n': 'H17', '86180224\r\n': 'H41', '76357A24\r\n': 'H52', 'A2D33D2E\r\n': 'H53', '86053724\r\n': 'H50', '9613AA24\r\n': 'H36', 'C4D21F23\r\n': 'H64', 'F483A923\r\n': 'H26', '2551C623\r\n': 'H60', 'D43A7E23\r\n': 'H27', 'D4132D23\r\n': 'H3', 'A5F7A422\r\n': 'H12', 'C4A75823\r\n': 'H37', '7293472E\r\n': 'I13', 'A59A7C22\r\n': 'I34', '729E212E\r\n': 'I31', 'F486FE23\r\n': 'I16', 'C4FDBC23\r\n': 'I23', '52FC1A2E\r\n': 'I42', 'B544BE22\r\n': 'I50', 'F47CE123\r\n': 'I20', 'E498D823\r\n': 'I36', 'D498C323\r\n': 'I24', '7259AF2E\r\n': 'I17', 'F46DB623\r\n': 'I48', '82687C2E\r\n': 'I44', '72909B2E\r\n': 'I18', '821AB92E\r\n': 'I6', 'F43A6823\r\n': 'I28', 'C215F42E\r\n': 'I52', 'E4F48E23\r\n': 'I25', '66975A24\r\n': 'I3', '8274DA2E\r\n': 'I45', '66F9A624\r\n': 'I54', '8242232E\r\n': 'I10', '82D2762E\r\n': 'I21', 'F4757923\r\n': 'I37', '667F8824\r\n': 'I2', '82EA812E\r\n': 'I5', 'A5BC8F22\r\n': 'I46', '8218F62E\r\n': 'I51', 'E4B41E23\r\n': 'I29', '66ACA824\r\n': 'I56', '72964C2E\r\n': 'I43', 'A56D7B22\r\n': 'I47', '76012D24\r\n': 'I53', '72D4B92E\r\n': 'I15', 'E43C9523\r\n': 'I60', '72C4B12E\r\n': 'I19', '76107624\r\n': 'I1', '768A5524\r\n': 'I58', '76DB2824\r\n': 'I4', 'E49E5723\r\n': 'I26', '76645624\r\n': 'I59', 'B5729122\r\n': 'I57', 'A599C822\r\n': 'I32', '820B8E2E\r\n': 'I8', '8269212E\r\n': 'I14', '8203C32E\r\n': 'I22', '86557024\r\n': 'I39', 'E4B72723\r\n': 'I12', 'F4047B23\r\n': 'I38', 'A5778A22\r\n': 'I33', '72C7D12E\r\n': 'I35', 'A575A722\r\n': 'I49', '728F182E\r\n': 'I9', 'E4564723\r\n': 'I40', 'F45FBD23\r\n': 'I11', '66A5E424\r\n': 'I55', 'D49EA923\r\n': 'I7', 'B57B6B22\r\n': 'I41', 'D4379F23\r\n': 'I30', 'E4ADC423\r\n': 'I27'}
active_beds = [ ]                                #fetch from main server





left_beds = ['D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D31', 'D32', 'D33', 'D34', 'D35', 'D36', 'D43', 'D44', 'D45', 'D46', 'D47', 'D48', 'D54', 'D55', 'D56', 'D57', 'D58', 'D59', 'D66', 'D67', 'D68', 'D69', 'D70', 'D71', 'D78', 'D79', 'D80', 'D81', 'D82', 'D83', 'D89', 'D90', 'D91', 'D92', 'D93', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C37', 'C38', 'C39', 'C40', 'C41', 'C42', 'C49', 'C50', 'C51', 'C52', 'C53', 'C54', 'C61', 'C62', 'C63', 'C64', 'C65', 'C66', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E18', 'E19', 'E20', 'E21', 'E22', 'E23', 'E30', 'E31', 'E32', 'E33', 'E34', 'E35', 'E40', 'E41', 'E42', 'E43', 'E44', 'E45', 'E46', 'E47', 'E54', 'E55', 'E56', 'E57', 'E58', 'E59', 'E65', 'E66', 'E67', 'E68', 'E69', 'E70', 'E77', 'E78', 'E79', 'E80', 'E81', 'E82', 'E89', 'E90', 'E91', 'E92', 'E93', 'E94', 'E101', 'E102', 'E103', 'E104', 'E105', 'E106', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F54', 'F55', 'F56', 'F57', 'F58', 'F59', 'F66', 'F67', 'F68', 'F69', 'F70', 'F71', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G13', 'G14', 'G15', 'G16', 'G17', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G36', 'G37', 'G38', 'G39', 'G40', 'G41','H1', 'H2', 'H3', 'H4', 'H5', 'H10', 'H11', 'H12', 'H13', 'H20', 'H21', 'H22', 'H23', 'H24', 'H25', 'H32', 'H33', 'H34', 'H35', 'H36', 'H37', 'H44', 'H45', 'H46', 'H47', 'H48', 'H49', 'H56', 'H57', 'H58', 'H59', 'H60', 'H61'] 





active_beds_temp = fetch_data.get_active_bed_data()
print(active_beds_temp)
active_beds = active_beds_temp.get('beds')
print(active_beds)

ser=serial.Serial("/dev/ttyACM0",19200,timeout=0.8)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 19200


turn_left = False
line_follow_mode = False
global bed
bed = 'none'


def line_follow_config(fn):
    leftend.when_activated = fn
    rightend.when_activated = fn
    center.when_activated = fn
    leftback.when_activated = fn
    rightback.when_activated = fn


    leftend.when_deactivated = fn
    rightend.when_deactivated = fn
    center.when_deactivated = fn
    leftback.when_deactivated = fn
    rightback.when_deactivated = fn


def stop_line_follow():
    global line_follow_mode
    line_follow_mode = False

def active_fetch():
    active_beds_temp = fetch_data.get_active_bed_data()
    print(active_beds_temp)
    active_beds = active_beds_temp.get('beds')
    print(active_beds)


def rfid_read():
    global turn_left
    global bed                                   #rfid taking and decisions
    print("RFID_READ")
    bed = rfid_dict[rfid_cpy]
    
    if (bed in active_beds):
        print("Active beds are detected")
        turn_left = bed in left_beds
        robot.stop()
        time.sleep(0.8)
        print("makin a turn for interaction")
        turn_robot()
    else:
        print("not in active beds list")
        print("not active_bed")
        # So that robot automatically moves on to next bed
        robot.forward()
        time.sleep(1)
        line_follow()

        
def turn_robot():

    robot.forward()
    time.sleep(0.3)
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    time.sleep(1)
    robot.stop()
    robot.forward()
    time.sleep(0.3)
    robot.stop()
    print("turn is here")



def mod_turn_robot():
    robot.forward()
    time.sleep(0.1)
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    print("turn is here")
    time.sleep(0.8)
    while True:
        if center.is_active:
           print("center_active")
           time.sleep(0.2)
           print("time_implemented")   #implement timne delay
           robot.stop()
           print("robot_stopped")
           break
    line_follow()




def rfid():
    global rfid_cpy
    ser.flushInput() # flushing out old data
    read_ser=ser.readline()
    print (read_ser)
    rfid_cpy = read_ser
    if read_ser in rfid_dict:
        stop_robot()
        print("detected and stopping robot")
        rfid_read()
    #else:
        #line_follow()


def check():
    

    if not line_follow_mode:
        return

    print(center.is_active , leftend.is_active , rightend.is_active)
    
    

    if center.is_active and rightend.is_active and leftend.is_active:
        print("cross_near")
        robot.forward()
        rfid()
        #return

    elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
        print("forward")
        robot.forward()

    elif (not leftend.is_active) and rightend.is_active:
        robot.right()
        print("right")

    elif leftend.is_active and (not rightend.is_active):
        robot.left()
        print("left")
    
    elif (not leftend.is_active) and (not rightend.is_active) and (not center.is_active):
        stop_robot



def line_follow():
    print("line_follow")

    global line_follow_mode
    line_follow_mode = True
    check()
    line_follow_config(check)

def examine():
    global turn_left                                        #examination_finish and continue
    turn_left = not turn_left
    mod_turn_robot()


def stop_robot():
    robot.stop()
    stop_line_follow()


def take_pressure():                                      #pressure taking button
    GPIO.output(5,0)
    time.sleep(0.1)
    GPIO.output(5,1)

def take_temp():
    GPIO.output(6,0)
    time.sleep(0.4)
    GPIO.output(6,1)

def spox():
    GPIO.output(26,0)
    time.sleep(0.5)
    GPIO.output(26,1)
    

def fwd():
    robot.forward()

def small_left():
    robot.left()
    time.sleep(0.4)
    robot.stop()

def small_right():
    robot.right()
    time.sleep(0.4)
    robot.stop()

robo_actions = {
    "forward": fwd,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": stop_robot,
    "line": line_follow,
    "examine": examine,
    "take_pressure": take_pressure,
    "take_temp": take_temp,
    "spox": spox,
    "active_fetch": active_fetch,
    "small_left": small_left,
    "small_right": small_right

}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html", bed_id = bed )

class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        movement = self.get_body_argument("movement")
        robo_actions[movement]()
        self.write("You wrote " + movement)

settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/move", CommandHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
