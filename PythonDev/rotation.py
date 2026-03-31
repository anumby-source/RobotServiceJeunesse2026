import cv2
import glob
import os
import xml.etree.ElementTree as ET

input_dir = "../dataset80/images/"
input_dir_xml = "../dataset80/xml/"

ROTATIONS = ("cw", "ccw")

output_dir = {
    'cw': "../dataset80/images_90_cw/",
    'ccw': "../dataset80/images_90_ccw/",
}
output_dir_xml = {
    'cw': "../dataset80/xml_90_cw/",
    'ccw': "../dataset80/xml_90_ccw/",
}

rotation = {
    'cw': cv2.ROTATE_90_CLOCKWISE,
    'ccw': cv2.ROTATE_90_COUNTERCLOCKWISE,
}


for rot in ROTATIONS:
    os.makedirs(output_dir[rot], exist_ok=True)
    os.makedirs(output_dir_xml[rot], exist_ok=True)


W, H = 320, 240  # dimensions originales


def rotate_bbox(xmin, ymin, xmax, ymax, rot):
    if rot == "cw":  # +90°
        new_xmin = H - ymax
        new_ymin = xmin
        new_xmax = H - ymin
        new_ymax = xmax

    elif rot == "ccw":  # -90°
        new_xmin = ymin
        new_ymin = W - xmax
        new_xmax = ymax
        new_ymax = W - xmin

    return new_xmin, new_ymin, new_xmax, new_ymax


for img_path in glob.glob(os.path.join(input_dir, "photo_*.jpg")):
    filename = os.path.basename(img_path)
    dirname = os.path.dirname(img_path)
    dirxmlname = dirname.replace("images", "xml")
    xml_path = os.path.join(dirxmlname, filename.replace("jpg", "xml"))

    print(f"==========> {input_dir} filename={filename} dirname={dirname} dirxmlname={dirxmlname} xml_path={xml_path}")

    img = cv2.imread(img_path)
    if img is None:
        print("Image illisible :", img_path)
        continue

    # rotation image
    for rot in ROTATIONS:
        rotated = cv2.rotate(img, rotation[rot])
        new_img_path = os.path.join(output_dir[rot], filename)
        print(new_img_path)
        cv2.imwrite(new_img_path, rotated)

    new_W, new_H = H, W

    # rotation annotation VOC
    for rot in ROTATIONS:
        try:
            print("xml_path=", xml_path)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            root.find("size/width").text = str(new_W)
            root.find("size/height").text = str(new_H)

            for obj in root.findall("object"):
                bnd = obj.find("bndbox")
                xmin = int(bnd.find("xmin").text)
                ymin = int(bnd.find("ymin").text)
                xmax = int(bnd.find("xmax").text)
                ymax = int(bnd.find("ymax").text)

                nxmin, nymin, nxmax, nymax = rotate_bbox(xmin, ymin, xmax, ymax, rot)

                bnd.find("xmin").text = str(nxmin)
                bnd.find("ymin").text = str(nymin)
                bnd.find("xmax").text = str(nxmax)
                bnd.find("ymax").text = str(nymax)

            new_xml_path = os.path.join(output_dir_xml[rot], filename.replace(".jpg", ".xml"))
            print(new_xml_path)
            tree.write(new_xml_path)

        except:
            print("xml_path=", xml_path, "not found")


