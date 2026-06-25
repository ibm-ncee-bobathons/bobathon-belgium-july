"""
Unit Tests for Todo Application API
Tests all endpoints with comprehensive coverage including edge cases and error scenarios.
"""

import unittest
import json
from app import app, db
from models import Todo
from datetime import datetime


class TodoAPITestCase(unittest.TestCase):
    """Test case for the Todo API endpoints"""
    
    def setUp(self):
        """Set up test client and in-memory database before each test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up database after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_sample_todo(self, title="Test Todo", description="Test Description", completed=False):
        """Helper method to create a sample todo"""
        with app.app_context():
            todo = Todo(title=title, description=description, completed=completed)
            db.session.add(todo)
            db.session.commit()
            return todo.id
    
    # ========================================================================
    # GET /api/todos - List all todos
    # ========================================================================
    
    def test_get_todos_empty(self):
        """Test getting todos when database is empty"""
        response = self.client.get('/api/todos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    def test_get_todos_with_data(self):
        """Test getting todos when database has data"""
        # Create sample todos
        self.create_sample_todo("Todo 1", "Description 1")
        self.create_sample_todo("Todo 2", "Description 2", completed=True)
        
        response = self.client.get('/api/todos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 2)
        self.assertIn('id', data[0])
        self.assertIn('title', data[0])
        self.assertIn('description', data[0])
        self.assertIn('completed', data[0])
        self.assertIn('created_at', data[0])
    
    def test_get_todos_ordering(self):
        """Test that todos are ordered by created_at descending"""
        # Create todos with slight delay
        id1 = self.create_sample_todo("First Todo")
        id2 = self.create_sample_todo("Second Todo")
        
        response = self.client.get('/api/todos')
        data = json.loads(response.data)
        
        # Second todo should be first (newest first)
        self.assertEqual(data[0]['id'], id2)
        self.assertEqual(data[1]['id'], id1)
    
    # ========================================================================
    # GET /api/todos/<id> - Get specific todo
    # ========================================================================
    
    def test_get_todo_by_id_success(self):
        """Test getting a specific todo by ID"""
        todo_id = self.create_sample_todo("Specific Todo", "Specific Description")
        
        response = self.client.get(f'/api/todos/{todo_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['id'], todo_id)
        self.assertEqual(data['title'], "Specific Todo")
        self.assertEqual(data['description'], "Specific Description")
        self.assertEqual(data['completed'], False)
    
    def test_get_todo_by_id_not_found(self):
        """Test getting a non-existent todo"""
        response = self.client.get('/api/todos/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    # ========================================================================
    # POST /api/todos - Create new todo
    # ========================================================================
    
    def test_create_todo_success(self):
        """Test creating a new todo with valid data"""
        payload = {
            'title': 'New Todo',
            'description': 'New Description'
        }
        
        response = self.client.post(
            '/api/todos',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'New Todo')
        self.assertEqual(data['description'], 'New Description')
        self.assertEqual(data['completed'], False)
        self.assertIn('created_at', data)
    
    def test_create_todo_without_description(self):
        """Test creating a todo without description (optional field)"""
        payload = {'title': 'Todo without description'}
        
        response = self.client.post(
            '/api/todos',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Todo without description')
        self.assertEqual(data['description'], '')
    
    def test_create_todo_missing_title(self):
        """Test creating a todo without required title field"""
        payload = {'description': 'Description without title'}
        
        response = self.client.post(
            '/api/todos',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('required', data['error'].lower())
    
    def test_create_todo_empty_payload(self):
        """Test creating a todo with empty payload"""
        response = self.client.post(
            '/api/todos',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_todo_no_json(self):
        """Test creating a todo without JSON content type"""
        response = self.client.post('/api/todos', data='not json')
        self.assertEqual(response.status_code, 400)
    
    def test_create_todo_empty_title(self):
        """Test creating a todo with empty string title"""
        payload = {'title': '', 'description': 'Description'}
        
        response = self.client.post(
            '/api/todos',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    # ========================================================================
    # PUT /api/todos/<id> - Update todo
    # ========================================================================
    
    def test_update_todo_all_fields(self):
        """Test updating all fields of a todo"""
        todo_id = self.create_sample_todo("Original Title", "Original Description")
        
        payload = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'completed': True
        }
        
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['id'], todo_id)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['description'], 'Updated Description')
        self.assertEqual(data['completed'], True)
    
    def test_update_todo_partial_title(self):
        """Test updating only the title"""
        todo_id = self.create_sample_todo("Original Title", "Original Description")
        
        payload = {'title': 'New Title Only'}
        
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['title'], 'New Title Only')
        self.assertEqual(data['description'], 'Original Description')
        self.assertEqual(data['completed'], False)
    
    def test_update_todo_partial_completed(self):
        """Test updating only the completed status"""
        todo_id = self.create_sample_todo("Title", "Description", completed=False)
        
        payload = {'completed': True}
        
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['completed'], True)
        self.assertEqual(data['title'], 'Title')
    
    def test_update_todo_toggle_completed(self):
        """Test toggling completed status multiple times"""
        todo_id = self.create_sample_todo("Toggle Test")
        
        # Toggle to True
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        self.assertEqual(json.loads(response.data)['completed'], True)
        
        # Toggle back to False
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({'completed': False}),
            content_type='application/json'
        )
        self.assertEqual(json.loads(response.data)['completed'], False)
    
    def test_update_todo_not_found(self):
        """Test updating a non-existent todo"""
        payload = {'title': 'Updated Title'}
        
        response = self.client.put(
            '/api/todos/999',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_update_todo_empty_payload(self):
        """Test updating with empty payload (should succeed, no changes)"""
        todo_id = self.create_sample_todo("Original", "Description")
        
        response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Original')
    
    # ========================================================================
    # DELETE /api/todos/<id> - Delete todo
    # ========================================================================
    
    def test_delete_todo_success(self):
        """Test deleting an existing todo"""
        todo_id = self.create_sample_todo("To Be Deleted")
        
        response = self.client.delete(f'/api/todos/{todo_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('deleted', data['message'].lower())
        
        # Verify todo is actually deleted
        get_response = self.client.get(f'/api/todos/{todo_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_todo_not_found(self):
        """Test deleting a non-existent todo"""
        response = self.client.delete('/api/todos/999')
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_delete_todo_verify_others_remain(self):
        """Test that deleting one todo doesn't affect others"""
        id1 = self.create_sample_todo("Todo 1")
        id2 = self.create_sample_todo("Todo 2")
        id3 = self.create_sample_todo("Todo 3")
        
        # Delete middle todo
        response = self.client.delete(f'/api/todos/{id2}')
        self.assertEqual(response.status_code, 200)
        
        # Verify others still exist
        response = self.client.get('/api/todos')
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        ids = [todo['id'] for todo in data]
        self.assertIn(id1, ids)
        self.assertIn(id3, ids)
        self.assertNotIn(id2, ids)
    
    # ========================================================================
    # GET /api/health - Health check
    # ========================================================================
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    # ========================================================================
    # Integration Tests
    # ========================================================================
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow"""
        # Create
        create_response = self.client.post(
            '/api/todos',
            data=json.dumps({'title': 'Workflow Test', 'description': 'Testing CRUD'}),
            content_type='application/json'
        )
        self.assertEqual(create_response.status_code, 201)
        todo_id = json.loads(create_response.data)['id']
        
        # Read
        read_response = self.client.get(f'/api/todos/{todo_id}')
        self.assertEqual(read_response.status_code, 200)
        
        # Update
        update_response = self.client.put(
            f'/api/todos/{todo_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertTrue(json.loads(update_response.data)['completed'])
        
        # Delete
        delete_response = self.client.delete(f'/api/todos/{todo_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify deletion
        verify_response = self.client.get(f'/api/todos/{todo_id}')
        self.assertEqual(verify_response.status_code, 404)
    
    def test_multiple_todos_operations(self):
        """Test operations with multiple todos"""
        # Create multiple todos
        ids = []
        for i in range(5):
            response = self.client.post(
                '/api/todos',
                data=json.dumps({'title': f'Todo {i}', 'description': f'Description {i}'}),
                content_type='application/json'
            )
            ids.append(json.loads(response.data)['id'])
        
        # Verify all created
        response = self.client.get('/api/todos')
        self.assertEqual(len(json.loads(response.data)), 5)
        
        # Update some
        for i in [0, 2, 4]:
            self.client.put(
                f'/api/todos/{ids[i]}',
                data=json.dumps({'completed': True}),
                content_type='application/json'
            )
        
        # Delete some
        for i in [1, 3]:
            self.client.delete(f'/api/todos/{ids[i]}')
        
        # Verify final state
        response = self.client.get('/api/todos')
        remaining = json.loads(response.data)
        self.assertEqual(len(remaining), 3)
        
        completed_count = sum(1 for todo in remaining if todo['completed'])
        self.assertEqual(completed_count, 3)
    
    def test_todo_model_to_dict(self):
        """Test the Todo model's to_dict method"""
        with app.app_context():
            todo = Todo(title="Test", description="Description", completed=False)
            db.session.add(todo)
            db.session.commit()
            
            todo_dict = todo.to_dict()
            
            self.assertIn('id', todo_dict)
            self.assertIn('title', todo_dict)
            self.assertIn('description', todo_dict)
            self.assertIn('completed', todo_dict)
            self.assertIn('created_at', todo_dict)
            self.assertIsInstance(todo_dict['created_at'], str)
    
    def test_todo_model_repr(self):
        """Test the Todo model's __repr__ method"""
        with app.app_context():
            todo = Todo(title="Test Todo", description="Description")
            db.session.add(todo)
            db.session.commit()
            
            repr_str = repr(todo)
            self.assertIn('Todo', repr_str)
            self.assertIn(str(todo.id), repr_str)
            self.assertIn('Test Todo', repr_str)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

# Made with Bob
