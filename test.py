__author__ = 'Agnieszka'
import os
import flaskapp
import unittest
import tempfile

class flaskappTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskapp.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flaskapp.app.test_client()
        flaskapp.connect_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskapp.app.config['DATABASE'])


    def test_create_tasks(self):
        return self.app.post('/add', data=dict(
        name = 'tasks',
        due_date = '2016-05-05',
        priority = '2'
    ), follow_redirects=True)


    def test_complete_tasks(self):
        self.app.get('tasks/', follow_redirects=True)
        self.test_create_tasks()
        response = self.app.get("complete/1/", follow_redirects=True)


    def test_delete_tasks(self):
        self.app.get('tasks/', follow_redirects=True)
        self.test_create_tasks()
        response = self.app.get("delete/1/", follow_redirects=True)



if __name__ == '__main__':
    unittest.main()