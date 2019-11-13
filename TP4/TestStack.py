import unittest
import unittest.mock
import os
from Stack import Stack

class TestQueue(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    #Test du chemin empty-pop-empty (C1)
    def test_path_empty_pop(self):
        stack = Stack(5, 5, 5)

        #Vérification de l'état initial
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertEqual(str(stack),"|")

        #Test du chemin à l'aide de la fonction pop
        self.assertRaises(ValueError, stack.pop)


    #Test du chemin empty-push-normal-pop-empty (C2)
    def test_path_empty_push_normal_pop_empty(self):
        stack = Stack(5,5,5)

        #Vérification de l'état initial
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertEqual(str(stack),"|")

        #Application de la transition
        stack.push("first")

        #Vérification de l'état "normal"
        self.assertFalse(stack.isEmpty())
        self.assertEqual(stack.size(), 1)
        self.assertFalse(stack.isFull())
        self.assertEqual(stack.peek(), "first")
        self.assertEqual(str(stack),"|first|")

        #Application de la transition
        self.assertEqual(stack.pop(),"first")

        #Vérification de l'état "empty"
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")


    #Test du chemin empty-(push-normal)*-(pop-normal)*-pop-empty (extension de C2)
    def test_path_multiple_push(self):

        #Testons divers choix de nombre d'éléments à ajouter puis retirer
        for elem in range(3, 10):
            stack = Stack(20, 20, 20)

            #Vérification de l'état initial
            self.assertTrue(stack.isEmpty())
            self.assertEqual(stack.size(), 0)
            self.assertFalse(stack.isFull())
            self.assertRaises(ValueError, stack.peek)
            self.assertEqual(str(stack),"|")

            s = "|"

            #Appliquons le push "elem" fois
            for k in range(1, elem):

                stack.push(k)
                s = "|"+str(k)+s

                #Vérification de l'état "normal"
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)
                self.assertEqual(str(stack),s)

            #Appliquons le pop "elem" fois
            for k in range(elem-1, 0, -1):

                #Vérification de l'état "normal"
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)

                self.assertEqual(stack.pop(), k)

        #Vérification de l'état "empty"
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")


    #Test du chemin empty-(push-normal)*-push-full-(pop-normal)*-pop-empty (C3)
    def test_push_to_full(self):

        #Testons divers choix de tailles
        for size in range(3, 10):
            stack = Stack(size, 20, 20)
            s = "|"

            #Vérification de l'état initial
            self.assertTrue(stack.isEmpty())
            self.assertEqual(stack.size(), 0)
            self.assertFalse(stack.isFull())
            self.assertRaises(ValueError, stack.peek)
            self.assertEqual(str(stack),"|")

            #Appliquons le push "size" fois
            for k in range(1, size):

                stack.push(k)
                s = "|"+str(k)+s

                #Vérification de l'état "normal"
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)
                self.assertEqual(str(stack), s)

            stack.push("last")

            #Vérification de l'état "full"
            self.assertFalse(stack.isEmpty())
            self.assertEqual(stack.size(), size)
            self.assertTrue(stack.isFull())
            self.assertEqual(stack.peek(), "last")

            #Application de la transition
            self.assertTrue(stack.pop(), "last")

            #Appliquons le pop "size" fois
            for k in range(size-1, 0, -1):

                #Vérification de l'état "normal"
                self.assertFalse(stack.isEmpty())
                self.assertEqual(stack.size(), k)
                self.assertFalse(stack.isFull())
                self.assertEqual(stack.peek(), k)

                self.assertEqual(stack.pop(), k)

        #Vérification de l'état "empty"
        self.assertTrue(stack.isEmpty())
        self.assertEqual(stack.size(), 0)
        self.assertFalse(stack.isFull())
        self.assertRaises(ValueError, stack.peek)
        self.assertRaises(ValueError, stack.pop)
        self.assertEqual(str(stack),"|")


    #Test du chemin empty-(push-normal)*-push-full-(push-full)*-(push-normal)*-push-full-(pop-normal)*-pop-empty (C4)
    def test_push_to_full_then_increment(self):

        #Testons diverses combinaisons de size, trial et increment
        for size in range(5, 10):
            for trial in range(5, 10):
                for increment in range(5, 10):
                    stack = Stack(size, trial, increment)
                    s = "|"

                    #Vérification de l'état initial
                    self.assertTrue(stack.isEmpty())
                    self.assertEqual(stack.size(), 0)
                    self.assertFalse(stack.isFull())
                    self.assertRaises(ValueError, stack.peek)
                    self.assertEqual(str(stack),"|")

                    #Appliquons le push "size" fois
                    for k in range(1, size):

                        stack.push(k)
                        s = "|"+str(k)+s

                        #Vérification de l'état "normal"
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), k)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), k)
                        self.assertEqual(str(stack), s)

                    stack.push("last")
                    s = "|last"+s

                    #Vérification de l'état "full"
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size)
                    self.assertTrue(stack.isFull())
                    self.assertEqual(stack.peek(), "last")
                    self.assertEqual(str(stack), s)

                    #Vérifions que stack lance une exception pour les trial premiers ajouts
                    for nb in range(1, trial):
                        self.assertRaises(ValueError, stack.push, "fail")

                        #Vérification de l'état "full"
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size)
                        self.assertTrue(stack.isFull())
                        self.assertEqual(stack.peek(), "last")
                        self.assertEqual(str(stack), s)

                    #Testons le dernier push erroné avant que la taille de la pile n'augmente
                    self.assertRaises(ValueError, stack.push, "fail")

                    #Vérification de l'état "normal"
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size)
                    self.assertFalse(stack.isFull())
                    self.assertEqual(stack.peek(), "last")
                    self.assertEqual(str(stack), s)

                    #Appliquons le push "increment" fois
                    for i in range(1, increment):

                        stack.push(i)
                        s = "|"+str(i)+s

                        #Vérification de l'état "normal"
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size+i)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), i)
                        self.assertEqual(str(stack),s)

                    stack.push("end")

                    #Vérification de l'état "full"
                    self.assertFalse(stack.isEmpty())
                    self.assertEqual(stack.size(), size+increment)
                    self.assertTrue(stack.isFull())
                    self.assertEqual(stack.peek(), "end")

                    self.assertEqual(stack.pop(), "end")

                    #Appliquons le pop "increment" fois
                    for i in range(increment-1, 0, -1):

                        #Vérification de l'état "normal"
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), size+i)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), i)

                        self.assertEqual(stack.pop(), i)

                    self.assertTrue(stack.pop(), "last")

                    #Appliquons le pop "size" fois
                    for k in range(size-1, 0, -1):

                        #Vérification de l'état "normal"
                        self.assertFalse(stack.isEmpty())
                        self.assertEqual(stack.size(), k)
                        self.assertFalse(stack.isFull())
                        self.assertEqual(stack.peek(), k)

                        self.assertEqual(stack.pop(), k)

                #Vérification de l'état "empty"
                self.assertTrue(stack.isEmpty())
                self.assertEqual(stack.size(), 0)
                self.assertFalse(stack.isFull())
                self.assertRaises(ValueError, stack.peek)
                self.assertRaises(ValueError, stack.pop)
                self.assertEqual(str(stack),"|")

if __name__ == '__main__':
    unittest.main()