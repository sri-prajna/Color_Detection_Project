import cv2
import pandas as pd

# Read the CSV file
colors_csv = 'colors.csv'
index_colors = ["color_name", "hex", "R", "G", "B"]
colors_data = pd.read_csv(colors_csv, names=index_colors, header=None)

# Read the image
pic_path = 'color1.jpg'  # Replace with your image path
pic = cv2.imread(pic_path)
pic = cv2.resize(pic, (800, 600))  # Resize for easy viewing

clicked = False
r = g = b = x_pos = y_pos = 0

# Function to calculate the closest color name
def get_color_names(R, G, B):
    min = float('inf')
    c_name = ""
    for i in range(len(colors_data)):
        d = abs(R - int(colors_data.loc[i, "R"])) + abs(G - int(colors_data.loc[i, "G"])) + abs(B - int(colors_data.loc[i, "B"]))
        if d <= min:
            min = d
            c_name = colors_data.loc[i, "color_name"]
    return c_name

# Mouse click event
def get_draw_function(event, x, y, flags, param):
    global b, g, r, x_pos, y_pos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = pic[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('Color_Detection')
cv2.setMouseCallback('Color_Detection', get_draw_function)

while True:
    cv2.imshow("Color_Detection", pic)
    if clicked:
        # Draw rectangle and text
        cv2.rectangle(pic, (20, 20), (750, 60), (b, g, r), -1)
        text = get_color_names(r, g, b) + f' R={r} G={g} B={b}'
        cv2.putText(pic, text, (50, 50), 2, 0.8, (255, 255, 255) if r+g+b < 400 else (0, 0, 0), 2)
        clicked = False

    # Exit on ESC
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
