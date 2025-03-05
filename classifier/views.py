from django.shortcuts import render
import joblib
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.http import JsonResponse


pipeline = joblib.load('trained_pipeline.pkl')

def create_probability_plot(class_names, probabilities):
    # Convert numpy arrays to lists if needed
    if hasattr(class_names, 'tolist'):
        class_names = class_names.tolist()
    if hasattr(probabilities, 'tolist'):
        probabilities = probabilities.tolist()
        
    # Clear any existing plots
    plt.clf()
    
    # Create the bar plot with smaller size
    plt.figure(figsize=(3, 2))  # Further reduced
    bars = plt.bar(range(len(class_names)), probabilities)
    
    # Customize the plot
    plt.title('Prediction Probabilities by Class')
    plt.xlabel('Classes')
    plt.ylabel('Probability (%)')
    plt.xticks(range(len(class_names)), class_names, rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot to a temporary buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode the image to base64 string
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic

def create_gauge_chart(accuracy):
    # Clear any existing plots
    plt.clf()
    
    # Create figure and axis with smaller size
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(4, 2))  # Reduced from (6, 3)
    
    # Convert accuracy to radians (0-100% -> 0-π)
    theta = np.pi * (accuracy / 100)
    
    # Create the gauge
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_theta_offset(np.pi/2)  # Start from top
    
    # Set the limits
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    
    # Create the colored bars
    colors = [(0.8, 0.2, 0.2), (0.9, 0.6, 0.2), (0.2, 0.8, 0.2)]  # Red, Yellow, Green
    bounds = [0, 50, 80, 100]
    norm = plt.Normalize(0, 100)
    
    # Add the colored arcs
    for i in range(len(bounds)-1):
        ax.barh([0], [np.pi], [0.6], 
                left=[np.pi * bounds[i]/100],
                color=[colors[i]], alpha=0.3)
    
    # Add the needle
    ax.plot([0, theta], [0, 0.5], color='black', linewidth=2)
    
    # Add percentage text
    ax.text(0, -0.2, f'{accuracy:.1f}%', 
            ha='center', va='center', 
            fontsize=20, fontweight='bold')
    
    # Remove unnecessary elements
    ax.set_rticks([])
    ax.grid(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode
    gauge_image = base64.b64encode(image_png).decode('utf-8')
    return gauge_image

def home(request):
    return render(request, 'classifier/home.html')

def predict(request):
    if request.method == 'POST':
        description = request.POST.get('description', '')
        if description:
            # Debug information
            print("Classes:", pipeline.classes_)
            print("Classes shape:", len(pipeline.classes_))
            
            # Get probability scores for each class
            probabilities = pipeline.predict_proba([description])[0]
            print("Probabilities shape:", len(probabilities))
            
            prediction = pipeline.predict([description])[0]
            
            # Get class names from the pipeline - handle both list and numpy array cases
            class_names = pipeline.classes_
            if hasattr(class_names, 'tolist'):
                class_names = class_names.tolist()
            
            # Convert probabilities to percentages and ensure they're Python lists
            prob_percentages = np.array(probabilities * 100).ravel().round(2)
            if hasattr(prob_percentages, 'tolist'):
                prob_percentages = prob_percentages.tolist()
            
            # Ensure we're using the correct number of classes and probabilities
            # Take only the probabilities that correspond to actual classes
            if len(class_names) < len(prob_percentages):
                prob_percentages = prob_percentages[:len(class_names)]
            
            # Create the probability plot
            plot_image = create_probability_plot(class_names, prob_percentages)
            
            # Ensure prediction is a Python native type
            if hasattr(prediction, 'tolist'):
                prediction = prediction.tolist()
            elif hasattr(prediction, 'item'):
                prediction = prediction.item()
            
            # Find the highest probability (confidence score)
            max_probability = float(np.max(probabilities) * 100)  # Convert to float
            confidence_level = "High" if max_probability > 80 else "Medium" if max_probability > 50 else "Low"
            
            # Create the gauge chart
            gauge_image = create_gauge_chart(max_probability)
            
            context = {
                'prediction': prediction,
                'class_names': class_names,
                'probabilities': prob_percentages,
                'plot_image': plot_image,
                'gauge_image': gauge_image,
                'max_probability': f"{max_probability:.1f}%",
                'confidence_level': confidence_level,
            }
            return render(request, 'classifier/home.html', context)
    
    return render(request, 'classifier/home.html')

def classify_text(request):
    if request.method == 'POST':
        # ... existing code ...
        
        # Clean and format the result list
        id_value = result[0].strip("'[]")
        class_name = result[1].strip("'[]")
        
        # Create formatted output with each item on a new line
        formatted_result = f"ID: {id_value}\nSınıf: {class_name}"
        
        context = {
            'result': formatted_result,  # Send formatted result
            'prob_plot': prob_plot,
            'gauge_plot': gauge_plot,
            'bar_chart': bar_chart
        }
        
        return JsonResponse(context)


