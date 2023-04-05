from PIL import Image

# The color applied on detected boats.
DEBUG_COLOR_DETECTION = (255, 0, 0, 255)

# Max value in RGBA.
MAX_RGBA_VALUE = 255

# Number of component in RGB value (r, g and b)
MAX_VALUE_RGB_COMP = 3

def detect(img_path, save_path, remove_boats, export_as_mask):
    '''
    str, str, bool, bool -> None
    Allows to detect the boats on a satellite imagery.
    '''
    if '\\' in save_path:
        save_path.replace('\\', '')

    # Open image.
    img = Image.open(img_path)

    # We keep in copy a version in 'L'.
    img_luminance = img.convert('L')
    
    dom_color = get_dominant_color(img)
    brightness = get_brightness_image(img)

    opti_tolerance = get_optimal_tolerance(brightness)

    # Main loop.
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            # Exectued for each pixels.
            pixel = img_luminance.getpixel((x, y))
            
            if not (0 <= pixel <= opti_tolerance):
                # Boat detected
                if remove_boats:
                    img.putpixel((x, y), dom_color)

                    # We allow ourselves to overflow a little on the edges
                    # (10 pixels here) to have a better result.
                    neighbours = get_neighbour_coordinates((x, y), 10)

                    for neighbour in neighbours:
                        img.putpixel(neighbour, dom_color)

                else:
                    img.putpixel((x, y), DEBUG_COLOR_DETECTION)

    if export_as_mask:
       export_detection_mask(img, save_path + '\Mask.PNG')

    # We save the image.
    img.save(save_path + '\Detection.PNG')

def export_detection_mask(img, save_path):
    '''
    PIL.Image, str -> None
    Build an image of the detection mask from the pixels
    pixels detected as boats.
    '''
    mask = Image.new('RGB', img.size)
    
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))

            if pixel == DEBUG_COLOR_DETECTION:
                mask.putpixel((x, y), pixel)
    
    mask.save(save_path)

def get_dominant_color(img):
    '''
    Pil.Image -> tuple(r, g, b)
    Returns the dominant color of the image.
    '''
    pixels = img.getdata()

    # We ingore the alpha channel.
    #                 r  g  b
    dominant_color = [0, 0, 0]

    for i in range(MAX_VALUE_RGB_COMP):
        for k in range(len(pixels)):
            dominant_color[i] = dominant_color[i] + pixels[k][i]

    for i in range(len(dominant_color)):
        dominant_color[i] = dominant_color[i] // len(pixels)

    return tuple(dominant_color)

def get_brightness_image(img):
    '''
    Pil.Image -> float/int
    Returns the global brightness of the image.
    '''
    copy_as_L = img.convert('L')

    histogram = copy_as_L.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for i in range(scale):
        ratio = histogram[i] / pixels
        brightness = brightness + ratio * (-scale + i)

    if brightness == MAX_RGBA_VALUE:
        return 1

    return brightness / scale

def get_optimal_tolerance(brightness):
    '''
    float/int -> int
    Returns the most suitable tolerance for the image.
    '''
    # The clearer the background (here the sea), the greater the tolerance should be
    # and reverse.
    if brightness * MAX_RGBA_VALUE > 65:
        return 100

    return 80

def get_neighbour_coordinates(coordinates, pixel_distance):
    '''
    Returns the coordinates of the 4 neighboring pixels of a pixel
    (top, bottom, right and left).
    ''' 
    top_coord = (coordinates[0], coordinates[1] - pixel_distance)
    bottom_coord = (coordinates[0], coordinates[1] + pixel_distance)
    right_coord = (coordinates[0] + pixel_distance, coordinates[1])
    left_coord = (coordinates[0] - pixel_distance, coordinates[1])
    
    return [top_coord, bottom_coord, right_coord, left_coord]

# Usage.
detect(
    img_path='Samples\Boat16.PNG',
    save_path='Output',
    remove_boats=False,
    export_as_mask=True
)
