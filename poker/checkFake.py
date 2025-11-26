#-*- encoding:utf-8 -*-
from itertools import chain
import os,re,time,math
from typing import List, Tuple


def extractXMLLeaves(xmlString: str) -> List[str]:
    # matches <...>...</...> with no '<' in the ...s
    uncollapsedLeafRegex = r'<[^(<|/)]+>[^<]*</[^<]+>'
    # matches <.../> with no '<' in the ...
    collapsedLeafRegex = r'<[^<]*/>'
    return list(chain.from_iterable(map(lambda p: re.findall(p, xmlString), [uncollapsedLeafRegex, collapsedLeafRegex])))


# Caveat: Returns empty string if attr not found
def getXMLNodeAttributeValue(xmlNode: str, attr: str) -> str:
    res = re.search(rf'{attr}="(.*)"', xmlNode)
    return res.group(1) if res else ""


def getXMLBound(xml_path):
    with open(f"{xml_path}", encoding='utf-8') as f:
        # Parse the xml file and find leaves
        xml = f.read()
        leaves = extractXMLLeaves(xml)
        NodeCenter = []
        for l in leaves:
            bounds = getXMLNodeAttributeValue(l, "bounds")
            if bounds:
                # bounds examples: "[0,96][224,320]" Note that 0 to 224 is the width, 96 to 320 is the height
                ((x1, y1), (x2, y2)) = re.findall(
                    r'\[([0-9]*),([0-9]*)[0-9]*]', bounds)
                x1, x2, y1, y2 = int(x1), int(
                    x2), int(y1), int(y2)

                # store the center of the node
                NodeCenter.append((x1, y1, x2, y2))
        return NodeCenter


def getPNGBound(png_path, pkg_name):
    cmd = 'python3 detect_img.py --weights runs/train/exp13/weights/best.pt --source ' + png_path + \
        ' --device 0 --nosave --project check_option --name ' + \
        pkg_name + ' --save-txt --exist-ok'
    os.system(cmd)

    start_time = time.time()  # start timing
    while (time.time() - start_time < 15):
        if os.path.exists('check_option/'+pkg_name+'/labels/'+os.path.splitext(os.path.basename(png_path))[0]+'.txt'):
            print("The txt-file exists.")
            break
        else:
            print("The file does not exist, waiting...")
            time.sleep(1)  # Check again after 1 second

    if(time.time() - start_time >= 15):
        print("There is no button detected.")
        return []
    # Open the detection results of the model - txt file.
    with open('check_option/'+pkg_name+'/labels/'+os.path.splitext(os.path.basename(png_path))[0]+'.txt') as f:
        lines = f.readlines()
        result = []
        for line in lines:
            line = line.strip('\n')
            line = line.split(' ')
            line = (int(i) for i in line)
            result.append(line)
    return result


def checkFakeButton(png_coords, xml_coords, max_distance):
    not_found_fake_button = False
    btn_detect = len(png_coords)
    match = 0
    for png_coord in png_coords:
        x1, y1, x2, y2 = png_coord
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        for xml_coord in xml_coords:
            x3, y3, x4, y4 = xml_coord
            if x3 <= mid_x <= x4 and y3 <= mid_y <= y4:
                distance = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
                if distance < max_distance:
                    # not_found_fake_button = True
                    match += 1
                    break

    if match == btn_detect:
        return True
    else:
        return False


def pkgCheck(pkg_path, pkg_name):
    

    # Traverse all sub-directories under the packagename directory
    for root, dirs, files in os.walk(pkg_path):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            # Traverse all the XML and PNG files in the current subdirectory and compare them
            for subroot, subdirs, subfiles in os.walk(subdir_path):
                for file in subfiles:
                    if file.endswith('.xml'):
                        xml_path = os.path.join(subroot, file)
                        png_path = os.path.join(
                            subroot, file.replace('.xml', '.png'))
                        # print(xml_path)
                        # print(png_path)
                        png_coords = getPNGBound(png_path, pkg_name)
                        xml_coords = getXMLBound(xml_path)
                        result = checkFakeButton(png_coords, xml_coords, 400)
                        res_txt = os.path.join('check_result',f'{pkg_name}.txt')
                        if result:
                            with open(res_txt, 'a') as f:
                                f.write(f'[{png_path}]---------No fake buttons here.\n')
                        else:
                            with open(res_txt, 'a') as f:
                                f.write(f'[{png_path}]---------Fake buttons here.\n')
                break


def batchCheck():
    # Get all the packagenames in the check_btn directory
    pkg_names = [name for name in os.listdir('check_btn') if os.path.isdir(os.path.join('check_btn', name))]

    # Traverse all the packagenames
    for pkg_name in pkg_names:
        # pkg_name = input('Enter the packagename: ')
        pkg_path = 'check_btn/' + pkg_name
        pkgCheck(pkg_path, pkg_name)

if __name__ == "__main__":
    batchCheck()