# sens-file-generatorNcompressor

check
http://graphics.stanford.edu/projects/bundlefusion/
this script(builder.py) compress color, depth, (pose), camera parameter to .sens file

to do that you can test your data generation is right for bundlefusion program.

please put depth image as 16bit image(which elt. has value in mm)
not relative disparity, or something like retrived from opencv stereovision block matcher
(I mean, this only work with absolute value png)
