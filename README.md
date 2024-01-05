# HuffmanEncoder  Main file: huffman.py
This project takes a given text file, creates a binary representation of each character, and compresses it. To do this, it parses through the text file and 
counts the number of occurrences of each ASCII character. Once the frequencies are calculated, an ordered doubly linked list is created. Each character in the file with its associated 
frequency is added to a Huffman node object which is then added to the list. Then a Huffman tree is constructed by continuously taking the bottom 2 nodes of the linked list and combining them.
This Huffman tree is then used to calculate the binary codes for each of the characters in the file based on the path the tree takes to reach the leaf that houses that character.
Once the codes are calculated, the codes replace each character in the file and the HuffmanBitWriter function is called to convert the codes into binary. 
A given compressed file can also be uncompressed and decoded using the Huffman Bit Writer and the header of the file which describes the each ascii character and its associated frequency.
