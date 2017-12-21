Generate Images Usage <br /> 
12/21/17 <br />
Dean Hutton <br />

# Summary
This guide illustrates how to run the generate_images.py program for creating images from raster data. 
Generate_images.py was built with Python 2.7.10 so it is recommended to use that version of the interpreter 
while running. If you are running on Mac OSX it will be installed by default. This can be checked by running 
```python ­V``` on the terminal. Any version of Python between 2.7 and including 2.9 will work fine with this program.
It is recommended to use a python Virtual Environment to run this application but it is not required.

# Required Python Libraries
In order to run generate_images.py the following Python libraries must be installed in your virtual environment. Again,
it is recommended to use a virtual environment to house all these libraries and install them via PIP. 

1. nose 1.3.7 - To run unit tests
2. pip 9.0.1 - To install Python libraries
4. setuptools - 38.23.3
5. six - 1.11.0
6. wsgiref - 0.1.2
7. numpy - 1.13.3 - For data processing
8. numexpr - 2.64
9. tables - 0.30.0 - For reading input data
10. Pillow - 4.3.0 - For creating images
11. olefile - 0.44


# Setup and Usage
1. Setup and install a Python 2.7.10 Virtual Environment (VE). If you are unsure of how to do this see [here](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) 
2. Clone the repo ```git clone https://github.com/jellyDean/challenge_statement.git ```
3. Open a terminal and CD in to your VE ``` cd /Users/deanhutton/workdir/Personal/Repos/challenge_statement/VE ```  
4. Activate the Virtual Environment ``` . activate.fish ```
5. Install the above Required Python Libraries via PIP
6. Navigate to the repo ``` cd /Users/deanhutton/workdir/Personal/Repos/challenge_statement ```
7. Run the script by executing ``` python generate_images.py -i sample_data.inp -ol rgb.png -ot rgb ``` where 
    * ­i is the location of your input file
    * -ol is output location of image being created. File extension must be .png, .jpg or .jpeg
    * -ot is the output image type either rgb or greyscale


# Running Tests
1. Follow steps 1-5 in the Setup and Usage section above
2. Navigate to the tests directory ``` cd /Users/deanhutton/workdir/Personal/Repos/challenge_statement/tests ```
3. Enter ``` nosetests ``` in terminal and push enter
4. 6 Unit tests will run