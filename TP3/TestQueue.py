import unittest
import unittest.mock
import os
from Queue import Queue

class TestQueue(unittest.TestCase):

    #on suppose que setup et teardown doivent etre presents par convention
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEmptyQueue(self):

        queue = Queue()

        self.assertFalse(queue.hasOne())
        self.assertTrue(queue.isEmpty())
        self.assertFalse(queue.isFull())
        self.assertEqual(queue.size(), 0)

    def testEmptyQueueRaisesValueErrorWhenCheckingFirstAndLast(self):
        self.assertRaises(ValueError, Queue().check_first)
        self.assertRaises(ValueError, Queue().check_last)

    def testEmptyQueueRaisesValueErorWhenDequeuing(self):
        self.assertRaises(ValueError, Queue().dequeue)

    def testQueueWithOneElementRaisesValueErrorWhenLastIsChecked(self):
        queue = Queue()
        queue.enqeue(1)
        self.assertTrue(queue.hasOne())
        self.assertRaises(ValueError, queue.check_last)

    def testEnqeueToMaxDoesNotThrowErrors(self):

        queue = Queue()
        queue.enqeue(0)

        for k in range(1, queue.MAX):
            self.assertFalse(queue.isFull())
            queue.enqeue(k)
            self.assertEqual(queue.size(), k+1)
            self.assertEqual(str(queue.check_last()), str(k))

        self.assertTrue(queue.isFull())

    def testEnqueueMoreThanMaxRaisesValueError(self):

        queue = Queue()

        for k in range(0, queue.MAX):
            queue.enqeue(k)

        self.assertRaises(ValueError, queue.enqeue, 0)

    def testDequeueReturnsExpectedValues(self):

        queue = Queue()

        for k in range(0, queue.MAX):
            queue.enqeue(k)

        tailleAttendue = queue.size()

        self.assertEqual(str(queue.check_first()), str(0))
        self.assertTrue(queue.isFull())
        self.assertEqual(queue.size(), tailleAttendue)

        self.assertEqual(str(queue.dequeue()), str(0))
        self.assertFalse(queue.isFull())
        tailleAttendue = tailleAttendue - 1
        self.assertEqual(queue.size(), tailleAttendue)

        for k in range(1, queue.MAX-1):
            self.assertEqual(str(queue.check_first()), str(k))
            self.assertEqual(str(queue.dequeue()), str(k))
            self.assertFalse(queue.isFull())

            tailleAttendue = tailleAttendue - 1
            self.assertEqual(queue.size(), tailleAttendue)

        self.assertEqual(queue.size(),1)
        self.assertTrue(queue.hasOne)
        self.assertRaises(ValueError, queue.check_last)
        
        self.assertEqual(str(queue.check_first()), str(99))
        self.assertEqual(str(queue.dequeue()), str(99))

        self.assertEquals(queue.size(),0)
        self.assertTrue(queue.hasOne)
        self.assertRaises(ValueError, queue.check_first)
        self.assertRaises(ValueError, queue.check_last)

if __name__ == '__main__':
    unittest.main()