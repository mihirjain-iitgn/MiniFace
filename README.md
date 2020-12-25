# Mini-Face
This project is a networking application that tries to mimic the functionality provided by facebook. The implementation is written from scratch using TCP sockets. 
The application uses a client-server architecture and the designed application level protocol is "stateless". More details can be found in this [pdf](https://drive.google.com/file/d/1qKasrZVxsc02BeVXpQIOya-A8x79Mu_P/view?usp=sharing) or this [video](https://drive.google.com/file/d/1T9fuKXXh0pTaNyMBNcaxWW3THw52yrut/view?usp=sharing).

## Set-up

 - Requirements :  `python 3.x`, `pip`.
 - Clone this repository. 
 - Get stdiomask `pip3 install stdiomask`
 - Run `python3 server.py` on one terminal and `python3 client.py` on another.
 
 **Note :** The client maintains a file to store the session id. So, to run multiple clients in one machine a copy of `client.py` must be made and be kept in a different directory.

## Authors

 - [Mihir Jain](https://github.com/mihirjain-iitgn)
 - [Priyam Tongia](https://github.com/Priyam1418)
