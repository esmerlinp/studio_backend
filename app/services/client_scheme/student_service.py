from app.models.client_scheme.student_model import Student
from app.models.client_scheme.student_details_models import (
    StudentFamily, StudentFamilyPhone, StudentFamilyEmail, 
    StudentAllergy, StudentMedicalPhone
)
from app.models.master_scheme.allergy_model import Allergy
from app import db
from datetime import datetime

def get_full_student_detail(student_id):
    """
    Retrieve full student details including family and medical info.
    """
    student = Student.query.get(student_id)
    if not student:
        return None
    
    # Base student info
    student_data = student.to_dict(include_sensitive=True)
    
    # Family info
    if student.familyId:
        family = StudentFamily.query.get(student.familyId)
        if family:
            family_data = family.to_dict()
            
            # Phones and Emails
            phones = StudentFamilyPhone.query.filter_by(familyId=family.id).all()
            emails = StudentFamilyEmail.query.filter_by(familyId=family.id).all()
            
            family_data['phones'] = [p.to_dict() for p in phones]
            family_data['emails'] = [e.to_dict() for e in emails]
            
            student_data['family'] = family_data
    
    # Allergies
    allergies = db.session.query(StudentAllergy, Allergy.name)\
        .join(Allergy, StudentAllergy.allergyId == Allergy.id)\
        .filter(StudentAllergy.studentId == student_id).all()
    
    student_data['allergies'] = [
        {"id": a.StudentAllergy.id, "allergyId": a.StudentAllergy.allergyId, "name": a.name}
        for a in allergies
    ]
    
    # Medical Phones
    med_phones = StudentMedicalPhone.query.filter_by(studentId=student_id).all()
    student_data['medicalPhones'] = [
        {"id": p.id, "phoneTypeId": p.phoneTypeId, "phoneNumber": p.phoneNumber}
        for p in med_phones
    ]
    
    return student_data

def save_student_detail(student_id, data):
    """
    Save/Update student details.
    """
    if student_id:
        student = Student.query.get(student_id)
        if not student:
            return None, "Estudiante no encontrado"
    else:
        student = Student()
        db.session.add(student)

    # Helper function for int conversion
    def to_int(val):
        if val is None or val == '': return None
        try: return int(val)
        except: return val

    # 1. Base Information
    student.firstName = data.get('firstName')
    student.middleName = data.get('middleName')
    student.lastName = data.get('lastName')
    student.secondLastName = data.get('secondLastName')
    
    # Dates handling
    if data.get('birthDate'):
        try:
            student.birthDate = datetime.fromisoformat(data['birthDate'].split('T')[0])
        except: pass
    if data.get('enrollmentDate'):
        try:
            student.enrollmentDate = datetime.fromisoformat(data['enrollmentDate'].split('T')[0])
        except: pass

    student.genderId = to_int(data.get('genderId'))
    student.courseId = to_int(data.get('courseId'))
    student.livingSituation = data.get('livingSituation')
    
    # Location
    student.countryId = to_int(data.get('countryId'))
    student.cityId = to_int(data.get('cityId'))
    student.sectorId = to_int(data.get('sectorId'))
    student.address = data.get('address')
    
    # Medical
    student.doctorName = data.get('doctorName')
    student.insuranceNumber = data.get('insuranceNumber')
    student.medicalInstitutionId = to_int(data.get('medicalInstitutionId'))
    student.insuranceInstitutionId = to_int(data.get('insuranceInstitutionId'))
    student.bloodTypeId = to_int(data.get('bloodTypeId'))
    
    # Academic/Others
    student.previousSchoolId = to_int(data.get('previousSchoolId'))
    student.entryReason = data.get('entryReason')
    student.exitReason = data.get('exitReason')

    # 2. Family Info
    family_data = data.get('family', {})
    if family_data:
        if not student.familyId:
            family = StudentFamily()
            db.session.add(family)
            db.session.flush() 
            student.familyId = family.id
        else:
            family = StudentFamily.query.get(student.familyId)
        
        family.responsibleType = to_int(family_data.get('responsibleType'))
        family.paymentFrequencyId = to_int(family_data.get('paymentFrequencyId'))
        
        # Father
        father = family_data.get('father', {})
        family.fatherFirstName1 = father.get('firstName1')
        family.fatherFirstName2 = father.get('firstName2')
        family.fatherLastName1 = father.get('lastName1')
        family.fatherLastName2 = father.get('lastName2')
        family.fatherDocument = father.get('document')
        family.fatherDocumentTypeId = to_int(father.get('documentTypeId'))
        family.fatherProfessionId = to_int(father.get('professionId'))
        family.fatherMaritalStatusId = to_int(father.get('maritalStatusId'))
        
        # Mother
        mother = family_data.get('mother', {})
        family.motherFirstName1 = mother.get('firstName1')
        family.motherFirstName2 = mother.get('firstName2')
        family.motherLastName1 = mother.get('lastName1')
        family.motherLastName2 = mother.get('lastName2')
        family.motherDocument = mother.get('document')
        family.motherDocumentTypeId = to_int(mother.get('documentTypeId'))
        family.motherProfessionId = to_int(mother.get('professionId'))
        family.motherMaritalStatusId = to_int(mother.get('maritalStatusId'))

        # Sync Phones
        phones = family_data.get('phones', [])
        StudentFamilyPhone.query.filter_by(familyId=family.id).delete()
        for p in phones:
            if p.get('phoneNumber'):
                new_phone = StudentFamilyPhone(
                    familyId=family.id,
                    phoneTypeId=to_int(p.get('phoneTypeId')),
                    phoneNumber=p.get('phoneNumber'),
                    isPrincipal=p.get('isPrincipal', False)
                )
                db.session.add(new_phone)

        # Sync Emails
        emails = family_data.get('emails', [])
        StudentFamilyEmail.query.filter_by(familyId=family.id).delete()
        for e in emails:
            if e.get('email'):
                new_email = StudentFamilyEmail(
                    familyId=family.id,
                    email=e.get('email'),
                    isPrincipal=e.get('isPrincipal', False)
                )
                db.session.add(new_email)

    db.session.commit()
    return student.id, None