import cv2
import numpy as np
from sklearn.cluster import KMeans

def get_dominant_color(image_path, k=1):
    # 1. קריאת התמונה מהדיסק
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found. Please check the path."
    
    # 2. המרת ייצוג הצבעים מ-BGR (של OpenCV) ל-RGB הסטנדרטי
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 3. שינוי מבנה מטריצת הפיקסלים לרשימה שטוחה של פיקסלים (כל פיקסל הוא 3 ערכי RGB)
    pixels = image.reshape((-1, 3))
    
    # 4. הגדרת מודל K-Means עם K אשכולות והרצתו על הפיקסלים
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    # 5. חילוץ מרכזי האשכולות (הצבעים הדומיננטיים ביותר שחולצו)
    dominant_colors = clt.cluster_centers_.astype(int)
    
    return dominant_colors.tolist()

# נקודת ריצה לבדיקת הסקריפט
if __name__ == "__main__":
    # ננסה לחלץ את הצבע הדומיננטי ביותר (K=1)
    # וגם את 3 הצבעים המובילים (K=3) כדי לראות את פלטת הצבעים של הפריט
    test_image = "test_item.jpg"
    
    print(f"--- Running Color Extractor on '{test_image}' ---")
    
    # שליחת בקשה לחילוץ הצבע המרכזי
    primary_color = get_dominant_color(test_image, k=1)
    print(f"Primary Dominant RGB Color (K=1): {primary_color}")
    
    # שליחת בקשה לחילוץ פלטת 3 הצבעים המרכזיים
    color_palette = get_dominant_color(test_image, k=3)
    print(f"Top 3 Palette Colors (K=3): {color_palette}")

# פונקציה חדשה להמרת RGB לפורמט HEX סטנדרטי
def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])

def get_dominant_color(image_path, k=1):
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found."
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape((-1, 3))
    
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    dominant_colors = clt.cluster_centers_.astype(int)
    return dominant_colors.tolist()

if __name__ == "__main__":
    test_image = "test_item.jpg"
    print(f"--- Running Upgraded Color Extractor on '{test_image}' ---")
    
    # חילוץ מערך ה-RGB המרכזי
    primary_rgb = get_dominant_color(test_image, k=1)[0]
    print(f"Primary RGB: {primary_rgb}")
    
    # המרה ל-HEX
    primary_hex = rgb_to_hex(primary_rgb)
    print(f"Primary HEX Vector: {primary_hex}")