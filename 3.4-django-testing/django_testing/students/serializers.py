from django.conf import settings

from rest_framework import serializers

from students.models import Course

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def create(self, validated_data):
        
        students_count = 0
        students = validated_data.get('students')
        
        if students:
            students_count = len(students)
        
        if students_count < settings.MAX_STUDENTS_PER_COURSE:
            return super().create(validated_data)
        
        raise serializers.ValidationError(f"The maximum number of students on course {students_count} has been exceeded")

        
    