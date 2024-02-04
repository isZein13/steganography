import matplotlib.pyplot as plt
import numpy as np
import os
import skimage
from skimage import io
from skimage import morphology, segmentation, color
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed, mark_boundaries
from skimage.util import img_as_float
import cv2
import math
from PIL import Image, ImageTk



# def iop_detect(photo):
    
#     file = os.path.join(skimage.data_dir, photo.image.path)
#     myimg = io.imread(file)

#     img = img_as_float(myimg[::2, ::2])

#     lum = color.rgb2gray(myimg)
#     mask = morphology.remove_small_holes(
#         morphology.remove_small_objects(lum < 0.7, 500),500)

#     mask = morphology.opening(mask, morphology.disk(3))
#     m_slic = segmentation.slic(myimg, n_segments=100, mask=mask, start_label=1)

#     fig, ax_arr = plt.subplots(1, 2)
#     fig.set_size_inches(16, 8, forward=True)
#     ax_arr[0].imshow(segmentation.mark_boundaries(myimg, m_slic))
#     ax_arr[0].contour(mask, colors='red', linewidths=1)
#     ax_arr[0].set_title("maskSLIC")
#     ax_arr[1].imshow(mask, cmap="gray")
#     ax_arr[1].set_title("Mask")

#     segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
#     segments_slic = slic(img, n_segments=250, compactness=10, sigma=1, start_label=1)
#     segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)
#     gradient = sobel(rgb2gray(img))
#     segments_watershed = watershed(gradient, markers=250, compactness=0.001)

#     sum = len(np.unique(segments_fz))+len(np.unique(segments_slic))+len(np.unique(segments_quick))
#     # if sum >= 450:
#     #     # photo.result = text
#     #     # 'IOP is Perhaps!\n'
#     #     # text_for_file = str(f"Felzenszwalb segments number: {len(np.unique(segments_fz))}" + '\n'
#     #     # f"SLIC segments number: {len(np.unique(segments_slic))}" + '\n'
#     #     # f"Quickshift segments numbe: {len(np.unique(segments_quick))}" + '\n'
#     #     # f"slicMask segments numbe: {len(np.unique(m_slic))}")
#     #     # photo.result += text_for_file
#     # elif sum <= 450:
#     #     # photo.result = text
#     #     # 'NOT IOP\n'
#     #     # text_for_file = str(f"Felzenszwalb segments number: {len(np.unique(segments_fz))}" + '\n'
#     #     #     f"SLIC segments number: {len(np.unique(segments_slic))}" + '\n'            
#     #     #     f"Quickshift segments numbe: {len(np.unique(segments_quick))}" + '\n'
#     #     #         f"slicMask segments numbe: {len(np.unique(m_slic))}")
#     #     # photo.result += text_for_file

#     photo.save()
#     fig, ax = plt.subplots(2, 2, figsize=(5, 5), sharex=True, sharey=True)

#     ax[0, 0].imshow(mark_boundaries(img, segments_fz))
#     ax[0, 0].set_title("Felzenszwalbs's method")
#     ax[0, 1].imshow(mark_boundaries(img, segments_slic))
#     ax[0, 1].set_title('SLIC')
#     ax[1, 0].imshow(mark_boundaries(img, segments_quick))
#     ax[1, 0].set_title('Quickshift')
#     ax[1, 1].imshow(mark_boundaries(img, segments_watershed))
#     ax[1, 1].set_title('Compact watershed')

#     for a in ax.ravel():
#         a.set_axis_off()

#     plt.tight_layout()

#     old_filename = os.path.basename(photo.image.path)
#     new_filename = os.path.basename(photo.image.path)

#     new_filename = new_filename[:new_filename.rfind('.')] + '_iop' + new_filename[new_filename.rfind('.'):]

#     plt.savefig(photo.image.path.replace(old_filename, new_filename))
    

def iop_encrypt(photo, user_text):
    print("Photo:",photo, photo.image)
    path_image =  photo.image.path
    print ('PATH:',path_image)
    data = user_text
    img = cv2.imread(path_image)
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    Pix = len(data) * 3

    Row = Pix/width
    Row = math.ceil(Row)

    count = 0
    charCounter = 0
    for i in range(Row + 1):
        while(count < width and charCounter < len(data)):
            char = data[charCounter]
            charCounter += 1
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCounter*3 < Pix and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCounter*3 >= Pix and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
        
    cv2.imwrite(path_image, img)
    return path_image
   
def iop_decrypt(photo_path):
    path_image = 'media/' + os.path.basename(photo_path)
    img = cv2.imread(path_image)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    message = []
    for i in range(int((len(data)+1)/8)):
        message.append(data[i*8:(i*8+8)])
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)

    return message