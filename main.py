from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    try:
        with open('patients.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file, indent=4)


@app.get("/health")
def read_root():
    return {"message": "The API is healthy!"}

@app.get("/")
def hello():
    return {"message": "Welcome to the Patient API!"}

@app.get("/about")
def about():
    return {
        "name": "Patient API",
        "version": "1.0.0",
        "description": "An API to manage patient data including BMI and health verdicts."
    }



@app.get("/view")
def view_patients():
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail="No patients found")
    return JSONResponse(content=data)


@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient to view")):
    data = load_data() 
    for key in data:
        if key == patient_id:
            return JSONResponse(data[patient_id])
    raise HTTPException(status_code=404, detail="Patient not found")
 

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query("asc", description="Order of sorting: asc or desc")): 
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    
    data = load_data()

    sort_order = True if order == "asc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=not sort_order)

    return JSONResponse(content=sorted_data)


@app.post("/create")
def create_patient(patient: Patient):
    
    #load existing data
    data = load_data() 

    # Check if patient already exists
    for key in data:
        if key  == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")  
        
    data[patient.id] = patient.model_dump(exclude='id')  # Exclude 'id' from the model dump
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully", "patient": patient.model_dump()})


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()   
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient = data[patient_id]
    updated_patient =  patient_update.model_dump(exclude_unset=True)  # Exclude unset fields
    for field, value in updated_patient.items():
        if value is not None:
            updated_patient[field] = value
    # Update only the fields provided in updated_patient, keep the rest from existing_patient
    for field, value in updated_patient.items():
        existing_patient[field] = value
    data[patient_id] = existing_patient
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully", "patient": existing_patient})
 
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data() 
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"})