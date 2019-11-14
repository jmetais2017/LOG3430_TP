import unittest
import unittest.mock
import os

#les imports se realisent selon l'ordre du ORD
from TestNode import TestNode
from TestLinkedList import TestLinkedList

from TestStack import TestStack
from TestAutoAdaptiveStack import TestAutoAdaptiveStack

from TestQueue import TestQueue
from TestAutoAdaptiveQueue import TestAutoAdaptiveQueue

from TestCalculator import TestCalculator

from TestScreenPrinter import TestScreenPrinter
from TestFilePrinter import TestFilePrinter

#pour tester toutes les classes
if __name__ == '__main__':
    unittest.main()