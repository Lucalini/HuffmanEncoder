import unittest
import subprocess
from ordered_list import *
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    def test_lt_and_eq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)
                    
                    
    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_huff_tree2(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 13)
        self.assertEqual(hufftree.char, ord(" "))
        left = hufftree.left
        self.assertEqual(left.freq, 6)
        self.assertEqual(left.char, ord(" "))
        right = hufftree.right
        self.assertEqual(right.freq, 7)
        self.assertEqual(right.char, ord("a"))
        
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
   
    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertEqual(codes[ord('z')], '')
        
    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        self.assertEqual(subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True), 0)
    def test_02_textfile(self):
        huffman_encode("file2.txt", "file2_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        self.assertEqual(subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell = True), 0)
        
    def test_WAP_textfile(self):
        huffman_encode("file_WAP.txt", "file_WAP_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        self.assertEqual(subprocess.call("diff -wb file_WAP_out_compressed.txt file_WAP_compressed_soln.txt", shell = True), 0)
    def test_DOI_textfile(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        self.assertEqual(subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt", shell = True), 0)


    def test_empty(self):
        freqlist = cnt_freq("empty_file.txt")
        self.assertEqual(freqlist, [0] * 256)
        self.assertEqual(create_huff_tree(freqlist), None)
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        self.assertEqual(subprocess.call("diff -wb empty_file_out.txt empty_file.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb empty_file_out_compressed.txt empty_file.txt", shell = True), 0)

    def test_single_val(self):
        freqlist = cnt_freq("single_val.txt")
        self.assertEqual(freqlist[10], 6)
        huffman_encode("single_val.txt", "single_val_out.txt")
        self.assertEqual(subprocess.call("diff -wb single_val_out.txt single_val_soln.txt", shell = True), 0)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("hi.txt", "bye.txt")
        with self.assertRaises(FileNotFoundError):
            huffman_decode("hi.txt", "bye.txt")

    def test_parse_header1(self):
        header_string = '1 5 2 9 3 12'
        ans = [5, 9, 12]
        test = parse_header(header_string)
        self.assertEqual(test[1:4], ans)

    def test_parse_header_empty(self):
        header_string = ''
        ans = [0] * 256
        test = parse_header(header_string)
        self.assertEqual(test, ans)

    def test_decode1(self):
        huffman_encode("file1.txt", "file1_out.txt")
        huffman_decode("file1_out_compressed.txt", "file1_decode.txt")
        self.assertEqual(subprocess.call("diff -wb file1_decode.txt file1.txt", shell = True), 0)

    def test_decode2(self):
        huffman_encode("file2.txt", "file2_out.txt")
        huffman_decode("file2_out_compressed.txt", "file2_decode.txt")
        self.assertEqual(subprocess.call("diff -wb file2_decode.txt file2.txt", shell = True), 0)

    def test_decode3(self):
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        huffman_decode("empty_file_out_compressed.txt", "empty_file_decode.txt")
        self.assertEqual(subprocess.call("diff -wb empty_file_decode.txt empty_file.txt", shell = True), 0)

    def test_decode4(self):
        huffman_encode("single_val.txt", "single_val_out.txt")
        huffman_decode("single_val_out_compressed.txt", "single_val_decode.txt")
        self.assertEqual(subprocess.call("diff -wb single_val_decode.txt single_val.txt", shell = True), 0)


    def test_decode_WAP(self):
        huffman_decode("file_WAP_out_compressed.txt", "file_WAP_decode.txt")
        self.assertEqual(subprocess.call("diff -wb file_WAP_decode.txt file_WAP.txt", shell = True), 0)
    
    def test_decode_DOP(self):
        huffman_decode("declaration_out_compressed.txt", "declaration_decode.txt")
        self.assertEqual(subprocess.call("diff -wb declaration_decode.txt declaration.txt", shell = True), 0)

if __name__ == '__main__': 
   unittest.main()
