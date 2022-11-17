# image-stiching
Input Image :
![image](https://user-images.githubusercontent.com/93991971/202370050-88b9a021-7429-4fff-a716-35001e2584e0.png)
Output Image :
![image](https://user-images.githubusercontent.com/93991971/202370099-5d66e412-c471-4fa6-9991-7d5b4ba51b3f.png)

List of steps :

    Calculate the key points and descriptions for sifting for both images;
    Calculate the distances between each image descriptor and another image descriptor;
    Select the top matches for each image descriptor;
    To evaluate homography, run RANSAC;
    Alight overlapping;
    Now stitch them.
    Compute the sift-key points and descriptors for left and right images;
    Compute distances between every descriptor in one image and every descriptor in the other image;
    Select the top best matches for each descriptor of an image;
    Run RANSAC to estimate homography;
    Warp to align for stitching;
    Finally, stitch them together.
