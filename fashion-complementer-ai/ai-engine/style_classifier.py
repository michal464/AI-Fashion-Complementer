import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def predict_style(image_path):
    # 1. טעינת התמונה ושינוי גודלה ל-(224, 224) - הגודל המדויק שרשת ResNet50 דורשת
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found."
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image, (224, 224))
    
    # 2. המרת התמונה למערך נומרי והוספת מימד ה-Batch (רשתות מצפות לקלט במבנה של מספר תמונות, גובה, רוחב, ערוצים)
    img_array = np.expand_dims(image_resized, axis=0)
    
    # 3. נרמול ערכי הפיקסלים בהתאם לפורמט שעליו אומנה רשת ResNet50 המקורית
    img_ready = preprocess_input(img_array)
    
    # 4. טעינת מודל ResNet50 עם משקולות מוכנות מראש (ImageNet)
    # include_top=False אומר שאנו מורידים את השכבה הסופית הכללית ומכינים אותה להוספת הסגנונות שלנו
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # הוספת שכבת פלט חדשה עבור 4 קטגוריות הסגנון של הפרויקט
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    predictions = tf.keras.layers.Dense(4, activation='softmax')(x) # 4 סגנונות
    
    model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)
    
    # 5. הגדרת שמות הסגנונות לפי סדר מערך הפלט
    classes = ['Casual', 'Formal', 'Sporty', 'Boho']
    
    # בשלב זה המודל עדיין לא עבר אימון (Fine-Tuning) על הדאטה-סט הספציפי, 
    # אך נריץ ניבוי ראשוני כדי לוודא שכל הצינור הארכיטקטוני של הטעינה והעיבוד עובד ללא שגיאות.
    preds = model.predict(img_ready)
    
    # חילוץ האינדקס בעל ההסתברות הגבוהה ביותר
    highest_class_idx = np.argmax(preds[0])
    
    return classes[highest_class_idx], preds[0].tolist()

if __name__ == "__main__":
    test_image = "test_item.jpg"
    print(f"--- Running Style Classifier on '{test_image}' ---")
    
    predicted_style, confidence_vector = predict_style(test_image)
    print(f"Predicted Style (Untrained Base): {predicted_style}")
    print(f"Confidence Vector (4 Styles): {confidence_vector}")