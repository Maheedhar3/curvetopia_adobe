# curvetopia_adobe
**Objective:** Mission is to identify, regularize, and beautify curves in 2D Euclidean
space.This project will also cover symmetry and curve completion techniques.

**Problem description:** Ideally we want a end to end process where we take a PNG (raster) image of a line art and output a set of curves, where the curves are defined as a connected sequence of cubic Bezier curves. ´ However to begin, we are allowed to make the following simplification. Instead of PNG as input, we will present line art in the form of polylines, which is defined as sequence
of points. To be precise, let a path be a finite sequence of point {pi}1≤i<=n from R2, and P be the set of all paths in R2. The input to our problem is finite subset of paths from P. The expected output is another set of paths with the necessary properties of regularization,
symmetry and completeness as defined in next sections. For visualization, we may use SVG format that can be rendered on a browser, and
the output curve can be in the form of cubic Bezier instead of polylines.


**Contributors:**
B. Maheedhar,
B. Amrutha,
Ch. Sai Jaswanth
