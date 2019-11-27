import unittest
import unittest.mock
import os
import io
import sys

from app import ScreenPrinter, LinkedList, Stack, Queue

class TestScreenPrinter(unittest.TestCase):

    def setUp(self):
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput  

    def tearDown(self):
        sys.stdout = sys.__stdout__  

    def testInit(self):
        for name in ["a", "b", "c", "d", "e"]:
            self.assertEqual(ScreenPrinter(name).name, name)

    def testVisitLogLinkedList(self):

        liste = LinkedList()

        for i in range(5):
            liste.append(i)

        liste.accept(ScreenPrinter(""))

        self.assertEqual(self.capturedOutput.getvalue(), "\n\n(0,1,2,3,4)\n\n")

    def testVisitLogStack(self):

        stack = Stack(10)

        for i in range(5):
            stack.push(i)

        stack.accept(ScreenPrinter(""))

        s="\n-------\n"
        expected = '\n'+s+'   4   '+s+'   3   '+s+'   2   '+s+'   1   '+s+'   0   '+s+'\n'

        self.assertEqual(self.capturedOutput.getvalue(), expected)

    def testVisitLogQueue(self):

        queue = Queue(10)

        for i in range(5):
            queue.enqueue(i)

        queue.accept(ScreenPrinter(""))

        self.assertEqual(self.capturedOutput.getvalue(), "\n\n|0|1|2|3|4|\n\n")

#pour tester ScreenPrinter uniquement
if __name__ == '__main__':
    unittest.main()