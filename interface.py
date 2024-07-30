import cv2
import numpy as np
import keras_ocr
from sympy import sympify

# Initialize a blank canvas
canvas = np.ones((400, 800), dtype="uint8") * 255
drawing = False
ix, iy = -1, -1

# Mouse callback function
def draw(event, x, y, flags, param):
    global ix, iy, drawing, canvas
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), 5)
            ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), 5)

# Function to recognize the drawn expression
def recognize_expression(canvas):
    image = cv2.cvtColor(canvas, cv2.COLOR_GRAY2RGB)
    image = cv2.resize(image, (800, 400))
    prediction_groups = pipeline.recognize([image])
    expression = ' '.join([text for text, box in prediction_groups[0]])
    return expression

# Function to parse and solve the recognized expression
def parse_and_solve(expression):
    try:
        result = sympify(expression)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

# Initialize the recognizer
pipeline = keras_ocr.pipeline.Pipeline()

# Create a window and set the mouse callback
cv2.namedWindow('Canvas')
cv2.setMouseCallback('Canvas', draw)

while True:
    cv2.imshow('Canvas', canvas)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Press 'ESC' to exit
        break
    elif k == ord('c'):  # Press 'c' to clear the canvas
        canvas[:] = 255
    elif k == ord('s'):  # Press 's' to solve the expression
        expression = recognize_expression(canvas)
        print("Recognized Expression:", expression)
        result = parse_and_solve(expression)
        if result is not None:
            print("Result:", result)
            cv2.putText(canvas, f'Result: {result}', (10, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Canvas', canvas)

cv2.destroyAllWindows()
