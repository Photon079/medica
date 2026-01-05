import os
import json
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Import your working Agent Graph
from agents.multiagent import app as agent_app 

def index(request):
    # 1. Load User Data from JSON
    # This simulates a database or profile fetch
    json_path = os.path.join(settings.BASE_DIR, 'data', 'user_data.json')
    user_context = {}
    
    try:
        with open(json_path, 'r') as f:
            user_context = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load user_data.json. Error: {e}")
        # Fallback defaults
        user_context = {
            "user_name": "Guest User",
            "user_initials": "GU",
            "persona": "Athlete"
        }

    # Prepare initial context for the template
    # This ensures the Header and Profile Badge show the correct info immediately
    context = {
        'user_name': user_context.get('user_name'),
        'user_initials': user_context.get('user_initials'),
        'persona': user_context.get('persona')
    }
    
    # 2. Handle Image Upload (POST)
    if request.method == 'POST' and request.FILES.get('product_image'):
        try:
            image_file = request.FILES['product_image']
            
            # Save to 'media/images'
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))
            filename = fs.save(image_file.name, image_file)
            file_path = fs.path(filename)
            
            # URL for the template to display the image
            file_url = f"{settings.MEDIA_URL}images/{filename}"
            
            # 3. Use Persona from JSON (Backend Source of Truth)
            # We ignore the POST request's persona to be safe
            active_persona = user_context.get('persona', 'Athlete')

            # 4. Run the AI Agent Council
            inputs = {
                "image_data": file_path,    # Note: agents/multiagent.py expects 'image_path'
                "user_persona": active_persona
            }
            
            result = agent_app.invoke(inputs)
            
            # 5. Update Context with Results
            context.update({
                'result': result,
                'ui_mode': result.get('ui_mode', 'TRADEOFF'),
                'image_url': file_url,
                # Ensure persona remains consistent
                'persona': active_persona 
            })
            
        except Exception as e:
            print(f"Error during processing: {e}")
            context['error'] = str(e)

    return render(request, 'index.html', context)