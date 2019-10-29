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


    #
    #tests pour l'attribut first
    #

    #tester le getter de first
    def testAttr_first_getter(self):
        self.assertRaises(ValueError, Queue().check_first)

        queue = Queue()
        queue.enqeue("test")

        self.assertEqual(str(queue.check_first()), "test")

    #tester le constructeur de first
    def testAttr_first_constructor(self):
        self.assertRaises(ValueError, Queue().check_first)

    #tester la fonction enqeue qui transforme lattribut first
    def testAttr_first_enqeue(self):
        queue = Queue()

        queue.enqeue(1)

        for i in range(2, 5):
            queue.enqeue(i)
            self.assertEqual(str(queue.check_first()), "1")

    
    #tester la fonction deqeue qui transforme lattribut first
    def testAttr_first_dequeue(self):
        queue = Queue()

        for i in range(1, 5):
            queue.enqeue(i)

        for i in range(1, 5):
            self.assertEqual(str(queue.dequeue()), str(i))


    #
    #Tests pour l'attribut last
    #

    #tester le getter de last
    def testAttr_last_getter(self):
        queue = Queue()

        self.assertRaises(ValueError, queue.check_last)

        queue.enqeue("a")
        self.assertRaises(ValueError, queue.check_last)

        queue.enqeue("b")
        self.assertEqual(str(queue.check_last()), "b")

    #tester le constructeur de last
    def testAttr_last_constructor(self):
        self.assertRaises(ValueError, Queue().check_last)

    #tester la methode enqueue qui modifie lattribut last
    def testAttr_last_enqueue(self):
        queue = Queue()
        queue.enqeue(1)
        queue.enqeue(2)

        for i in range (3, 10):
            queue.enqeue(i)
            self.assertEqual(str(queue.check_last()), str(i))

    #tester la methode dequeue qui modifie lattribut last
    def testAttr_last_dequeue(self):
        queue = Queue()
        queue.enqeue(1)
        queue.enqeue(2)

        for i in range (3, 10):
            queue.enqeue(i)

        for i in range (3, 10):
            queue.dequeue()
            self.assertEqual(str(queue.check_last()),str(9))

        for i in range(0, 2):
            queue.dequeue()
            self.assertRaises(ValueError, queue.check_last)

        self.assertRaises(ValueError, queue.dequeue)


    #
    #Tests pour l'attribut n
    #

    #tester le getter de n ( size() )
    def testAttr_n_getter(self):
        self.assertEqual(Queue().size(), 0)

    #tester le 2e getter de n ( hasOne() )
    def testAttr_n_hasOne(self):
        queue = Queue()
        self.assertFalse(queue.hasOne())
        queue.enqeue(1)
        self.assertTrue(queue.hasOne())
        queue.enqeue(2)
        self.assertFalse(queue.hasOne())

    #tester le constructeur de n
    def testAttr_n_constructor(self):
        self.assertEqual(Queue().size(), 0)

    #tester la methode enqueue qui modifie lattribut n
    def testAttr_n_enqeue(self):
        queue = Queue()

        for i in range(1, 10):
            queue.enqeue(i)
            self.assertEqual(queue.size(), i)
    
    #tester la methode dequeue qui modifie lattribut n
    def testAttr_n_dequeue(self):
        queue = Queue()

        for i in range(1, 10):
            queue.enqeue(i)

        for i in range(8, 0, -1):
            queue.dequeue()
            self.assertEqual(queue.size(), i)

    
    #
    #Tests pour l'attribut Full
    #

    #tester le getter de full
    def testAttr_full_getter(self):
        self.assertFalse(Queue().isFull())

    #tester le constructeur de full
    def testAttr_full_constructor(self):
        self.assertFalse(Queue().isFull())

    #tester la methode enqueue qui modifie l'attribut full
    def testAttr_full_enqeue(self):
        queue = Queue()

        for i in range(1, Queue.MAX):
            queue.enqeue(i)
            self.assertFalse(queue.isFull())

        queue.enqeue("fin")
        self.assertTrue(queue.isFull())

        self.assertRaises(ValueError, queue.enqeue, "impossible")

    #tester la methode dequeue qui modifie l'attribut full
    def testAttr_full_dequeue(self):
        queue = Queue()

        for i in range(0, Queue.MAX):
            queue.enqeue(i)

        self.assertTrue(queue.isFull())

        for i in range(0, Queue.MAX):
            queue.dequeue()
            self.assertFalse(queue.isFull())


    #
    #Tests pour l'attribut empty
    #

    #tester le getter de empty
    def testAttr_empty_getter(self):
        self.assertTrue(Queue().isEmpty())

    #tester le constructeur de empty
    def testAttr_empty_constructor(self):
        self.assertTrue(Queue().isEmpty())

    #tester la methode enqeue qui modifie l'attribut empty
    def testAttr_empty_enqeue(self):
        queue = Queue()

        self.assertTrue(queue.isEmpty())

        for i in range (0, 10):
            queue.enqeue(i)
            self.assertFalse(queue.isEmpty())

    #tester la methode dequeue qui modifie l'attribut empty
    def testAttr_empty_dequeue(self):
        
        for s in range(5, 10):
            queue = Queue()

            self.assertTrue(queue.isEmpty())

            for i in range(0, s):
                queue.enqeue(i)
                
            for i in range(0, s):
                self.assertFalse(queue.isEmpty())
                queue.dequeue()

            self.assertTrue(queue.isEmpty())

if __name__ == '__main__':
    unittest.main()