# FakeData

## The program

The source code in python3 is provided on the Github page. Binaries are also available for [Linux](https://www.dropbox.com/s/3135uw0q0b7ugj4/interactive?dl=0), [MacOS](https://www.dropbox.com/sh/5sd4xacgenyv8o7/AAAkSOxzOwqL00cr2Uj_njhna?dl=0) and [Windows](https://www.dropbox.com/s/o6uqvg8ni5xpmu9/interactive.exe?dl=0).

Notes:
1. If a PUMF is provided, values for continuous and discrete variables are drawn (unweighted, with replacement) from the PUMF variables values
2. If a PUMF is not provided or for variables that are not included in the PUMF, variables' values are drawn as follows: log-normal for continuous variables and uniform for discrete variables. Character variables simply take the name of the variable as value.
3. Some discrete variables are coded as discrete by Statistics Canada, but nonetheless take on decimal values. This is incompatible with Stata which require integer values. In most cases, this is not really an issue since the associated labels are simply equal to the value of the variable. Ex: value 1.01 has label "1.01" (Here State cannot associate a label to the non-integer value 1.01). Accordingly, the .do file will issue an error code. Simply commenting-out the associated line will solve the issue.

## How to Create Fake datasets from Statistics Canada Master Files (RDC)

Statistics Canada offers a large variety of datasets through its Research Data Center (RDC) program. However, since the analysis of the data has to be performed in one of its RDC, the development of codes is challenging. Indeed, for most of us, an Internet access is essential to the development of (moderately) complex codes.

Here, I provide a program that allows to generate fake data using Statistics Canada Master files, which are available through Nesstar. The program generates (random) variables with the same name and labels as the confidential files. Those fake datasets can be used to develop codes outside the RDC (debugging, performance testing...).

In order to use the code, please proceed as follows:

1. Download the Fakedata program

2. Recover the .xml file of the wanted survey on Nesstar (e.g. http://nesstar.library.ubc.ca/webview/)
   + "Statistics Canada metadata for Master Files (RDC)"
     + <Survey/Year/Cycle of you choice>
       + "Metadata"
         + "Other Documentation"
           + \<survey IMDB\>
             1. Click on the "download" button (floppy disk on the upper-right corner of the screen)
             2. Select "In xml format" Download

3. (Optional) Recover the .csv for the Public Use Microdata file (PUMF) of the corresponding survey (e.g. through ODESI)

4. Run the Fakedata program. The code will  ask for the .xml and .csv (if PUMF is provided). It will produce a .csv file of fake data as well as a .do file (Stata script) which contains the labels. To use those files, simply import the .csv in Stata and run the .do file.

