import unittest
import unittest.mock
import os

from app import FilePrinter, LinkedList, Stack, Queue

class TestFilePrinter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove("./test.txt")
        except IOError:
            pass

    def testInit(self):
        for filepath in ["test.txt", "lol.txt", "read.txt"]:
            for name in ["a", "b", "c", "d", "e"]:
                printer = FilePrinter(filepath, name)
                self.assertEqual(printer.file_path, filepath)
                self.assertEqual(printer.name, name)

    def testVisitLogLinkedList(self):

        liste = LinkedList()

        for i in range(5):
            liste.append(i)

        liste.accept(FilePrinter("./test.txt",""))

        with open('./test.txt', 'r') as myfile:
            result=myfile.read()

        self.assertEqual(result, "\n(0,1,2,3,4)\n")

    def testVisitLogStack(self):

        stack = Stack(10)

        for i in range(5):
            stack.push(i)

        stack.accept(FilePrinter("./test.txt",""))

        with open('./test.txt', 'r') as myfile:
            result=myfile.read()

        s="\n-------\n"
        expected = s+'   4   '+s+'   3   '+s+'   2   '+s+'   1   '+s+'   0   '+s

        self.assertEqual(result, expected)

    def testVisitLogQueue(self):

        queue = Queue(10)

        for i in range(5):
            queue.enqueue(i)

        queue.accept(FilePrinter("./test.txt",""))

        with open('./test.txt', 'r') as myfile:
            result=myfile.read()

        self.assertEqual(result, "\n|0|1|2|3|4|\n")

#pour tester FilePrinter uniquement
if __name__ == '__main__':
    unittest.main()