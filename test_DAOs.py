import sqlite3
import unittest
import unittest.mock
import os
from models import Contact
from DAOs import ContactDAO

# To complete...
class TestContactDAO(unittest.TestCase):

    def setUp(self):
        self.db_file = 'temp.db'
        self.contactDAO = ContactDAO(self.db_file)
        self.contactDAO.init_db()

    def tearDown(self):
        os.remove(self.db_file)
    
    def test_when_init_db_is_called_it_should_create_table(self):
        try:
            with sqlite3.connect(self.db_file) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM contact')
        except sqlite3.OperationalError:
            self.fail("Should not have raised sqlite3.OperationalError")
    
    
    def test_when_add_is_called_it_should_return_an_autoincremented_id(self):
        
        #On teste diverses valeurs de l'id à créer
        for i in range(1, 10):
            #On crée le i-ème contact à ajouter
            contact = Contact(0, "Name"+str(i), "lastName"+str(i), 111+i, "mail"+str(i), True, "date")
            #On vérifie que le i-ème contact est ajouté avec un id égal à i
            self.assertEqual(self.contactDAO.add(contact), i)
    
    
    def test_get_by_id_after_add_should_return_inserted_value(self):
        
        #On crée un contact à ajouter
        contact = Contact(0, "Name", "lastName", 111, "mail", True, "date")
        #On ajoute ce contact au DAO, puis on récupère son id
        id = self.contactDAO.add(contact)
        
        #On va chercher dans le DAO le contact ayant l'id obtenu ci-dessus, et on vérifie champ par champ qu'il est égal à notre contact initial
        self.assertEqual(self.contactDAO.get_by_id(id).first_name, "Name")
        self.assertEqual(self.contactDAO.get_by_id(id).last_name, "lastName")
        self.assertEqual(self.contactDAO.get_by_id(id).phone, '111')
        self.assertEqual(self.contactDAO.get_by_id(id).mail, "mail")
        self.assertTrue(self.contactDAO.get_by_id(id).updated)
        self.assertEqual(self.contactDAO.get_by_id(id).updated_date, "date")
        
    
    def test_get_by_names_after_add_should_return_inserted_value(self):
        
        #On crée un contact à ajouter
        contact = Contact(0, "Name", "lastName", 111, "mail", True, "date")
        #On ajoute ce contact au DAO
        id = self.contactDAO.add(contact)
        
        #On va chercher dans le DAO le contact ayant les noms donnés ci-dessus, et on vérifie champ par champ qu'il est égal à notre contact initial
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").id, id)
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").first_name, "Name")
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").last_name, "lastName")
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").phone, '111')
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").mail, "mail")
        self.assertTrue(self.contactDAO.get_by_names("Name", "lastName").updated)
        self.assertEqual(self.contactDAO.get_by_names("Name", "lastName").updated_date, "date")


    def test_get_by_id_with_undefined_rowid_should_return_None(self):
        
        #On tente de récupérer un contact sans en avoir ajouté au préalable
        self.assertEqual(self.contactDAO.get_by_id(1), None)
    
    
    def test_get_by_names_with_notexisted_contact_should_return_None(self):
        
        contact = Contact(0, "Denis", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On tente de récupérer un contact ne figurant pas dans le DAO
        self.assertEqual(self.contactDAO.get_by_names("Pierre", "Richard"), None)
    
    
    def test_deactivate_contact_then_get_it_with_id_should_be_not_updated(self):
        
        #On crée un contact pour les besoins du test, puis on l'ajoute
        contact = Contact(0, "Pierre", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On désactive ce contact
        self.contactDAO.deactivate(id)
        #On tente de récupérer ce contact, puis on vérifie qu'il n'a pas été updated
        self.assertFalse(self.contactDAO.get_by_id(id).updated)
        
    
    def test_deactivate_contact_on_undefined_id_should_return_zero(self):
        
        #On tente de désactiver un contact sans en avoir ajouté au préalable
        self.assertEqual(self.contactDAO.deactivate(1), 0)
    
    
    def test_after_deleting_contact_by_id_get_it_with_id_should_return_None(self):
        
        #On crée un contact pour les besoins du test, puis on l'ajoute
        contact = Contact(0, "Pierre", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On supprime ce contact
        self.contactDAO.delete_by_id(id)
        #On tente de récupérer ce contact par son id
        self.assertEqual(self.contactDAO.get_by_id(id), None)


    def test_deleting_undefined_id_should_return_zero(self):
        
        #On tente de supprimer un contact sans en avoir ajouté au préalable
        self.assertEqual(self.contactDAO.delete_by_id(1), 0)


    #Fail
    def test_after_deleting_contact_by_names_get_item_with_id_should_return_None(self):
        
        #On crée un contact pour les besoins du test, puis on l'ajoute
        contact = Contact(0, "Pierre", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On supprime ce contact
        self.contactDAO.delete_by_names("Pierre", "Richard")
        #On tente de récupérer ce contact par son id
        self.assertEqual(self.contactDAO.get_by_id(id), None)
        

    def test_deleting_not_existed_contact_should_return_zero(self):
        
        contact = Contact(0, "Denis", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On tente de supprimer un contact ne figurant pas dans le DAO
        self.assertEqual(self.contactDAO.delete_by_names("Pierre", "Richard"), 0)
        self.assertEqual(self.contactDAO.delete_by_id(15), 0)
        

    def test_update_contact_should_set_the_provided_values(self):
        
        #On crée un contact pour les besoins du test, puis on l'ajoute
        contact = Contact(0, "Pierre", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On définit les valeurs pour la modification
        contact = Contact(id, "Jean", "Martin", 222, "mail2", True, "date2")
        #On met à jour le contact initial
        count = self.contactDAO.update(contact)
        
        #On récupère le contact modifié, puis on vérifie qu'il contient les nouvelles valeurs
        self.assertEqual(self.contactDAO.get_by_id(id).first_name, "Jean")
        self.assertEqual(self.contactDAO.get_by_id(id).last_name, "Martin")
        self.assertEqual(self.contactDAO.get_by_id(id).phone, '222')
        self.assertEqual(self.contactDAO.get_by_id(id).mail, "mail2")
        self.assertTrue(self.contactDAO.get_by_id(id).updated)
        self.assertEqual(self.contactDAO.get_by_id(id).updated_date, "date2")
        
        

    def test_update_contact_should_return_zero_if_id_does_not_exist(self):
        
        #On définit les valeurs pour la modification
        contact1 = Contact(1, "Jean", "Martin", 222, "mail2", True, "date2")
        contact2 = Contact(10, "Jean", "Martin", 222, "mail2", True, "date2")
        contact3 = Contact(24, "Jean", "Martin", 222, "mail2", True, "date2")
        
        #On tente de mettre à jour les contacts aux id spécifiés
        self.assertEqual(self.contactDAO.update(contact1), 0)
        self.assertEqual(self.contactDAO.update(contact2), 0)
        self.assertEqual(self.contactDAO.update(contact3), 0)
        

    def test_list_contacts_with_no_contacts_added_returns_empty_list(self):
        
        #On liste les contacts sans en avoir ajouté au préalable
        #On teste toutes les valeurs possibles pour l'argument "updated"
        self.assertEqual(self.contactDAO.list(), [])
        self.assertEqual(self.contactDAO.list(True), [])
        self.assertEqual(self.contactDAO.list(False), [])
    
    
    def test_list_contacts_with_one_contact_should_return_list_with_contact(self):
        
        #On crée un contact pour les besoins du test, puis on l'ajoute
        contact = Contact(0, "Pierre", "Richard", 111, "mail", True, "date")
        id = self.contactDAO.add(contact)
        
        #On vérifie qu'on obtient une liste de longueur 1 contenant ce contact
        self.assertEqual(len(self.contactDAO.list()), 1)
        self.assertEqual(self.contactDAO.list()[0].first_name, "Pierre")
        self.assertEqual(self.contactDAO.list()[0].last_name, "Richard")
        self.assertEqual(self.contactDAO.list()[0].phone, '111')
        self.assertEqual(self.contactDAO.list()[0].mail, "mail")
        self.assertTrue(self.contactDAO.list()[0].updated)
        self.assertEqual(self.contactDAO.list()[0].updated_date, "date")
        
    
    def test_list_contacts_with_updated_False_and_all_items_updated_should_return_empty_list(self):
        
        #On ajoute plusieurs contacts, tous avec updated = True
        for i in range(1, 10):
            contact = Contact(0, "Name"+str(i), "lastName"+str(i), 111+i, "mail"+str(i), True, "date")
            id = self.contactDAO.add(contact)
            
        #On vérifie que l'on ne liste aucun contact en passant False en argument
        self.assertEqual(self.contactDAO.list(False), [])

    
    def test_list_contacts_with_updated_True_and_all_items_not_updated_should_return_empty_list(self):
        
        #On ajoute plusieurs contacts, tous avec updated = False
        for i in range(1, 10):
            contact = Contact(0, "Name"+str(i), "lastName"+str(i), 111+i, "mail"+str(i), False, "date")
            id = self.contactDAO.add(contact)
            
        #On vérifie que l'on ne liste aucun contact en passant True en argument
        self.assertEqual(self.contactDAO.list(True), [])
    
    
    def test_list_contacts_with_all_not_updated_items_and_updated_False_should_return_all_contacts(self):
        
        #On ajoute 9 contacts, tous avec updated = False
        for i in range(1, 10):
            contact = Contact(0, "Name"+str(i), "lastName"+str(i), 111+i, "mail"+str(i), False, "date")
            id = self.contactDAO.add(contact)
            
        #On vérifie qu'on obtient une liste de longueur 9
        self.assertEqual(len(self.contactDAO.list(False)), 9)


    def test_list_contacts_with_all_updated_items_and_updated_True_should_return_all_contacts(self):
        
        #On ajoute 9 contacts, tous avec updated = True
        for i in range(1, 10):
            contact = Contact(0, "Name"+str(i), "lastName"+str(i), 111+i, "mail"+str(i), True, "date")
            id = self.contactDAO.add(contact)
            
        #On vérifie qu'on obtient une liste de longueur 9
        self.assertEqual(len(self.contactDAO.list(True)), 9)

if __name__ == '__main__':
    unittest.main()
    
