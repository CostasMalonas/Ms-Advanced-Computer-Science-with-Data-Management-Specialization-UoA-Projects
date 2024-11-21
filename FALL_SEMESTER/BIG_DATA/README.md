# KEY VALUE STORE WITH TRIE STRUCTURE

## 1. First create data with the following command:


- python genData.py [-k K] [-n N] [-d D] [-l L] [-m M]


** e.g: python genData.py -k keyFile.txt -n 4 -d 5 -l 4 -m 3 **


## ** 2. Execute the kvServer.py program. For each server open a different terminal and run the program with a host and a port that exist in the serverFile.txt. The server program executes with the following command **:


- python kvServer.py [-a A] [-p P]


** e.g: python kvServer.py -a 127.0.0.1 -p 8062 **


## ** 3. Execute the client program with the following command **:
        

- python kvClient.py [-s S] [-i I] [-k K]


** e.g: python kvClient.py -s serverFile.txt -i dataToIndex.txt -k 2 **


        
## ** IMPORTANT NOTE **:
- Sometimes when executing the client script the program freezes when loading the data (If we want to load e.g 3000 rows). Please close the terminals, open new ones and t
