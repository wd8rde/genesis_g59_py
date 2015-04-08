# genesis_g59_py
Python module to control Genesis G59 Software Defined Radio transceiver.
See http://www.genesisradio.com.au/G59/

To install:
```bash
$ git clone https://github.com/wd8rde/genesis_g59_py.git
$ cd genesis_g59_py
$ python setup.py build
$ sudo python setup.py install
```

If you look at the  genesis_g59_py source, it has several directories, the top directory is just stuff to install the code on your computer, the genesis_g59 directory has the code to connect to the radio and send the command over usb, and the g59_si570 directory is code for calculating the register values for the Si570 DDS, which is how the frequency is set in the genesis protocol. The importatnt files are g59_usb.py, si570_utils.py, and sidefs.py.
```
├── genesis_g59
│   ├── g59_si570
│   │   ├── __init__.py
│   │   ├── si570_utils.py
│   │   └── sidefs.py
│   ├── g59_usb.py
│   └── __init__.py
├── LICENSE
├── README.md
└── setup.py
```
 So, if you have installed it, you can:
```python
$ python
> from genesis_g59 import *
> g = g59_cmd()
> g.set_filt(4)
> g.set_freq(14.3)
```
And this will set the bandpass filters to 30-20m, and the frequency to the Maritime Net, 14.300 Mhz.
