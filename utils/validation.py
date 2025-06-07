# utils/validation.py
def validate_pferd(pferd: dict) -> bool:
    required = ['Name', 'Gewicht', 'Alter']
    return all(f in pferd and pferd[f] for f in required)
