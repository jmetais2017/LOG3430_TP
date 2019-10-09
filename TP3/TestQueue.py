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

    #tests pour une queue vide
    def testEmptyQueue(self):

        queue = Queue()

        self.assertFalse(queue.hasOne())
        self.assertTrue(queue.isEmpty())
        self.assertFalse(queue.isFull())
        self.assertEqual(queue.size(), 0)

    #tests permettant de verifier qu'une queue vide lance une erreur
    #si on essaie d'obtenir le premier ou le dernier element
    def testEmptyQueueRaisesValueErrorWhenCheckingFirstAndLast(self):
        self.assertRaises(ValueError, Queue().check_first)
        self.assertRaises(ValueError, Queue().check_last)

    #test permettant de verifier qu'une queue vide lance une erreur
    #si on essaie de retirer un element
    def testEmptyQueueRaisesValueErorWhenDequeuing(self):
        self.assertRaises(ValueError, Queue().dequeue)

    #test permettant de verifier qu'une queue avec un element n'est pas
    #consideree a avoir un dernier element et qu'elle lance une erreur
    #si on l'essaie d'obtenir
    def testQueueWithOneElementRaisesValueErrorWhenLastIsChecked(self):
        queue = Queue()
        queue.enqeue(1)
        self.assertTrue(queue.hasOne())
        self.assertRaises(ValueError, queue.check_last)

    #test permettant de verifier qu'il est possible d'ajouter des elements
    #tant que ca ne depasse pas la capacite maximale permise
    def testEnqeueToMaxDoesNotThrowErrors(self):

        queue = Queue()
        queue.enqeue(0)

        for k in range(1, queue.MAX):
            self.assertFalse(queue.isFull())
            queue.enqeue(k)
            self.assertEqual(queue.size(), k+1)
            self.assertEqual(str(queue.check_first()), str(0))
            self.assertEqual(str(queue.check_last()), str(k))

        #on s'assure que la pile est considere pleine si on a
        #mis la quantite maximale d'elements permis
        self.assertTrue(queue.isFull())

    #test permettant de verifier que la queue lance une erreur
    #si on essaie d'ajouter un element alors que la nombre maximal
    #d'elements est deja atteint
    def testEnqueueMoreThanMaxRaisesValueError(self):

        queue = Queue()

        for k in range(0, queue.MAX):
            queue.enqeue(k)

        self.assertRaises(ValueError, queue.enqeue, 0)

    #test peremettant de s'assurer que les fonctions check_first
    #et deqeue fonctionnent comme prevu alors que la pile se fait
    #depiler
    def testCheckFirstAndDequeueReturnsExpectedValues(self):

        queue = Queue()

        for k in range(0, queue.MAX):
            queue.enqeue(k)

        tailleAttendue = queue.size()

        #tests pour le premier element
        self.assertEqual(str(queue.check_first()), str(0))
        self.assertEqual(str(queue.check_last()), str(99))
        self.assertTrue(queue.isFull())
        self.assertEqual(queue.size(), tailleAttendue)

        self.assertEqual(str(queue.dequeue()), str(0))
        self.assertFalse(queue.isFull())
        tailleAttendue = tailleAttendue - 1
        self.assertEqual(queue.size(), tailleAttendue)

        #tests pour les elements intermediaires
        for k in range(1, queue.MAX-1):
            self.assertEqual(str(queue.check_last()), str(99))
            self.assertEqual(str(queue.check_first()), str(k))
            self.assertEqual(str(queue.dequeue()), str(k))
            self.assertFalse(queue.isFull())

            tailleAttendue = tailleAttendue - 1
            self.assertEqual(queue.size(), tailleAttendue)

        #tests pour le dernier element
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