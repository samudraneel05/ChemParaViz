import pandas as pd
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Dataset, Equipment


def process_csv(file, user):
    """
    Process uploaded CSV file and create dataset with equipment records
    """
    # Read CSV file
    if isinstance(file, InMemoryUploadedFile):
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
    else:
        df = pd.read_csv(file)
    
    # Validate required columns
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain columns: {', '.join(required_columns)}")
    
    # Calculate summary statistics
    total_count = len(df)
    avg_flowrate = float(df['Flowrate'].mean())
    avg_pressure = float(df['Pressure'].mean())
    avg_temperature = float(df['Temperature'].mean())
    
    # Equipment type distribution
    type_distribution = df['Type'].value_counts().to_dict()
    
    # Create dataset
    dataset = Dataset.objects.create(
        user=user,
        filename=file.name,
        file=file,
        total_count=total_count,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature,
        equipment_type_distribution=type_distribution
    )
    
    # Create equipment records
    equipment_list = []
    for _, row in df.iterrows():
        equipment = Equipment(
            dataset=dataset,
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=float(row['Flowrate']),
            pressure=float(row['Pressure']),
            temperature=float(row['Temperature'])
        )
        equipment_list.append(equipment)
    
    Equipment.objects.bulk_create(equipment_list)
    
    # Keep only last 5 datasets per user
    user_datasets = Dataset.objects.filter(user=user).order_by('-uploaded_at')
    if user_datasets.count() > 5:
        datasets_to_delete = user_datasets[5:]
        for ds in datasets_to_delete:
            ds.file.delete()
            ds.delete()
    
    return dataset


def get_dataset_summary(dataset):
    """
    Get comprehensive summary of a dataset
    """
    equipment = dataset.equipment.all()
    
    summary = {
        'total_count': dataset.total_count,
        'averages': {
            'flowrate': round(dataset.avg_flowrate, 2),
            'pressure': round(dataset.avg_pressure, 2),
            'temperature': round(dataset.avg_temperature, 2)
        },
        'equipment_type_distribution': dataset.equipment_type_distribution,
        'equipment_details': []
    }
    
    for eq in equipment:
        summary['equipment_details'].append({
            'equipment_name': eq.equipment_name,
            'equipment_type': eq.equipment_type,
            'flowrate': eq.flowrate,
            'pressure': eq.pressure,
            'temperature': eq.temperature
        })
    
    return summary
