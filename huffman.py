from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if isinstance(other, HuffmanNode):
            return self.char == other.char
        else:
            return False

        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq == other.freq:
            return self.char < other.char
        else:
            return self.freq < other.freq

def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    f = open(filename, "r")
    running_cnt = [0] * 256
    for line in f:
        for character in line:
            running_cnt[ord(character)] +=1
    f.close()
    return running_cnt

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node o
    if the Huffman tree'''
    olist = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            olist.add(HuffmanNode(i, char_freq[i]))
    if olist.size() == 0:
        return None

    while olist.size() >= 2:
        huff1 = olist.pop(0)
        huff2 = olist.pop(0)

        if huff1.freq == huff2.freq:
            comb = HuffmanNode(huff1.char, huff1.freq + huff2.freq)
            comb.left = huff1
            comb.right = huff2

        elif huff1.freq < huff2.freq:
            if huff1.char > huff2.char:
                comb = HuffmanNode(huff2.char, huff1.freq + huff2.freq)

            if huff1.char < huff2.char:
                comb = HuffmanNode(huff1.char, huff1.freq + huff2.freq)
            comb.left = huff1
            comb.right = huff2
        olist.add(comb)

    huffman_tree = olist.pop(0)
    return huffman_tree


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    huff_tree = node
    huff_codes = [""]*256
    create_code_helper(huff_tree, huff_codes, "")
    return huff_codes
def create_code_helper(current_node, huff_codes, running_code):
    if current_node.right == None and current_node.left == None:
        huff_codes[current_node.char] = running_code
    else:
        create_code_helper(current_node.left, huff_codes, running_code + "0")
        create_code_helper(current_node.right, huff_codes, running_code + "1")


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header = ""
    for i in range(len(freqs)):
        if freqs[i] > 0:
            header += f" {i} {freqs[i]}"
    return header[1:]


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    inf = open(in_file, "r")
    characters = inf.read()
    outf = open(out_file, "w")
    if characters == "":
        outf.write("")
        compressed = HuffmanBitWriter(f"{out_file[:len(out_file)-4]}_compressed.txt")
        compressed.write_str("")
        inf.close()
        outf.close()
        compressed.close()
        return

    count_freq = cnt_freq(in_file)
    huffman_tree = create_huff_tree(count_freq)
    code = create_code(huffman_tree)
    header = create_header(count_freq)

    going_string = ""
    header_string = f"{header}\n"
    for char in characters:
        going_string += f"{code[ord(char)]}"
    outf.write(header_string)
    outf.write(going_string)
    outf.close()
    inf.close()

    compressed = HuffmanBitWriter(f"{out_file[:len(out_file)-4]}_compressed.txt")
    compressed.write_str(header_string)
    compressed.write_code(going_string)
    compressed.close()

def huffman_decode(encoded_file, decode_file):
    f = HuffmanBitReader(encoded_file)
    of = open(decode_file, "w")
    header_str = f.read_str()
    freq_list = parse_header(header_str)
    tree = create_huff_tree(freq_list)
    num_chars = 0
    for freq in freq_list:
        num_chars += freq

    for i in range(num_chars):
        current = tree

        while current.left is not None and current.right is not None:
            bit = f.read_bit()
            if bit:
                current = current.right
            if not bit:
                current = current.left

        of.write(chr(current.char))
    f.close()
    of.close()

def parse_header(header_string):
    header_split = header_string.split()
    freq_list = [0] * 256
    for i in range(0, len(header_split), 2):
        freq_list[int(header_split[i])] = int(header_split[i + 1])

    return freq_list



