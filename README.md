# ethiSSH

ethiSSH brute forces its way to victim's system by connecting & controlling the SSH session interactively through weak passwords or to a passwordless SSH server that relies upon a public key cryptograph.
And then it can be used to control multiple compromised hosts simultaneously.

## Overview

This script demonstrates how SSH brute force attacks work and provides a botnet-like behavior. It consists of two main components :

1. **ssh_pass:** The script can attempt to authenticate to a target host using weak passwords from a password list or
it brute forces through each of the 32,767 keys in order to
authenticate to a passwordless SSH server that relies upon a public-key cryptograph.

2. **botnet.py** The script showcases a basic botnet-like behavior, where multiple remote hosts (bots) are controlled from a central location.

## Getting Started

### Prerequisites

- Python 3.x (https://www.python.org/downloads/)
- `pxssh` library 
- `pyfiglet` library

[Download 1024-bit keys](http://www.exploit-db.com/exploits/5720/)


### Dependencies

- Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Installation

Clone the repository

```bash
git clone https://github.com/your-username/ethiSSH.git
cd ethiSSH
```

## Usage

### Brute forcing passwords

To brute force SSH credentials:
- either provide password list

```python
python ssh_pass.py -H target_host -u username -F password_list
```

- or provide keys list

```python
python ssh_pass.py -H target_host -u username -F keys_list
```

### Botnet behaviour

1. Run botnet.py without any arguments
```python
python botnet.py
```
The script will iterate over these three hosts & issue simulatenous commands to each of the victims.


## Important notes

- This script is intended for educational purposes and ethical use only. Always ensure you have proper authorization before testing any security-related scripts.

- Ensure network connectivity to the target hosts.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)