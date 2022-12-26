import pytest
import random

from rest_framework import status

from rest_framework.test import APIClient

from students.models import Course, Student

from model_bakery import baker

# START: БЛОК ОПРЕДЕЛЕНИЯ ФИКСТУР
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def courses_fabric():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    
    return factory

@pytest.fixture
def students_fabric():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    
    return factory

# END: БЛОК ОПРЕДЕЛЕНИЯ ФИКСТУР

# START: Блок тестов Course
@pytest.mark.django_db
def test_retrieve_course(client, courses_fabric, students_fabric):
    # Arrange
    student = students_fabric(_quantity=1,
    )
    course = courses_fabric(students=student, 
                            _quantity=1
    )
    course_id = course[0].id    
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data.get('id') == course_id

@pytest.mark.django_db  
def test_list_course(client, courses_fabric, students_fabric):
    # Arrange
    course_qty = 100
    student = students_fabric(_quantity=5,
    )
    course = courses_fabric(students=student, 
                            _quantity=course_qty
    )
    
    # Act
    response = client.get('/api/v1/courses/')
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == len(course)

@pytest.mark.django_db  
def test_filter_id_course(client, courses_fabric, students_fabric):
    # Arrange
    course_qty = 70
    student = students_fabric(_quantity=5
    )
    course = courses_fabric(students=student, 
                            _quantity=course_qty
    ) 
    course_id = random.randint(0, course_qty)

    # Act
    response = client.get(f'/api/v1/courses/', data={'id': course_id})
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data[0].get('id') == course_id

@pytest.mark.django_db 
def test_filter_name_course(client, courses_fabric, students_fabric):
 # Arrange
    course_qty = 200
    student = students_fabric(_quantity=25
    )
    course = courses_fabric(students=student, 
                            _quantity=course_qty
    ) 
    course_id = random.randint(0, course_qty)
    course_name = course[course_id].name

    # Act
    response = client.get('/api/v1/courses/', data={'name': course_name})
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data[0].get('id') == course_id + 1

@pytest.mark.django_db 
def test_create_course(client):
    # Arrange
    course_data = {
        'name': 'New course'
    }
    
    # Act
    response = client.post('/api/v1/courses/', data=course_data)
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db 
def test_patch_course(client, courses_fabric, students_fabric):
    # Arrange
    course_qty = 1
    student = students_fabric(_quantity=5
    )
    course = courses_fabric(students=student, 
                            _quantity=course_qty
    ) 
    new_course_name = 'My super course'
    data = {
        'name': new_course_name
    }
    course_id = course[0].id
    
    # Act
    response = client.patch(f'/api/v1/courses/{course_id}/', data=data)
    ret_data = response.json()
      
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert ret_data.get('name') == new_course_name
    
@pytest.mark.django_db 
def test_delete_course(client, courses_fabric, students_fabric):
    # Arrange
    course_qty = 1
    student = students_fabric(_quantity=5
    )
    course = courses_fabric(students=student, 
                            _quantity=course_qty
    ) 
    course_id = course[0].id
    
    # Act
    response = client.delete(f'/api/v1/courses/{course_id}/')
    
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db 
def test_max_students_create_course(client, students_fabric, settings):
    # Arrange
    course_qty = 1
    students = students_fabric(_quantity=1
    )
    
    post_data = {
        'name': 'New course',
        'students': [student.id for student in students]
        # Тут вот так сделал, потому что сериализатор почему-то не проходил проверку
        # А во внутрь не получилось посмотреть, 
        # хотя в настройках стоит, что можно весь код смотреть...
    }
    
    # Для тестирования изменяется количество пользователей на 1
    settings.MAX_STUDENTS_PER_COURSE = 2
    
    # Act
    response = client.post('/api/v1/courses/', data=post_data)
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED

# END: Блок тестов Course


