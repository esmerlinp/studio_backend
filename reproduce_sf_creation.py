
import os
from app import create_app, db
from app.models.master_scheme.screen_functionality_model import ScreenFunctionality

# Setup app context
app = create_app()

def test_create_sf():
    with app.app_context():
        # HARDCODED IDs based on expectation or previous query
        # I will start with dummy values and rely on the script to fail or succeed
        # Ideally I should fetch valid ones first. I'll fetch them inside the script.
        
        from app.models.master_scheme.screen_model import Screen
        from app.models.master_scheme.functionality_model import Functionality
        from app.models.master_scheme.module_model import Module  # Required for Screen FK resolution
        
        # db.session.execute(text("SET search_path TO master")) # Enforced by model args?
        
        screen = Screen.query.first()
        func = Functionality.query.first()
        
        if not screen or not func:
            print("No screen or functionality found")
            return

        print(f"Testing with Screen {screen.id} and Func {func.id}")
        
        if not screen or not func:
            print("No screen or functionality found")
            return

        print(f"Testing with Screen {screen.id} and Func {func.id}")
        
        # Check if already exists
        existing = ScreenFunctionality.query.filter_by(screen_id=screen.id, functionality_id=func.id).first()
        if existing:
            print(f"SF already exists (ID: {existing.id}). Deleting to test creation...")
            db.session.delete(existing)
            db.session.commit()

        print("Creating new SF...")
        try:
            sf = ScreenFunctionality(screen_id=screen.id, functionality_id=func.id, is_active=True)
            db.session.add(sf)
            db.session.commit()
            print("Success! Created SF ID:", sf.id)
            print("Dict:", sf.to_dict()) 
        except Exception as e:
            print("Caught Exception during create/commit/access:")
            print(f"Type: {type(e)}")
            print(e)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_create_sf()
