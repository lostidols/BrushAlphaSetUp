# BrushAlphaSetUp
Quickly sets up rendering for making brush alphas for sculpting in Blender.
Brush Alpha Addon v1.0 It can be found in the bottom of the Texture Tab in Properties.

This is a small addon I made to set up rendering for a brush alpha. 
Brush alphas are useful in sculpting for adding fine details. 
They're also super useful for mold making: because they project onto the 
surface of your sculpt, they can't create undercuts.

https://github.com/lostidols/BrushAlphaSetUp/blob/main/BASetup.png

What It Does

The addon quickly sets up your scene to render a black & white height map in 
Open EXR format. 

1-Positions an orthographic camera with 1080 x 1080 resolution
2-Sets output as a lossless , B&W .exr file (but does not save it.) Open EXR 
  is the format that gives you an artifact free height map.
3-Sets up the Mist Pass in layers, world, and camera display.
4-Creates compositor nodes to use and adjust the mist pass.
5-Turns on XRay mode so you can see mist range for adjustments.

After running the addon, hit Ctrl + Alt + 0 to look through the camera and 
scale your object to fit. Then, adjust the depth of the mist pass with the 
sliders in the addon panel so that it aligns with the top & bottom of your object. 
Toggle XRay with Alt + X if you need to. Then hit render, and save the image.
