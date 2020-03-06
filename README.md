# FakeData

## Create Fake datasets from Statistics Canada Master Files (RDC)

Statistics Canada offers a large variety of datasets through its Research Data Center (RDC) program. However, since the analysis of the data has to be performed in one of its RDC, the development of codes is challenging. Indeed, for most of us, an Internet access is essential to the development of (moderately) complex codes.

Here, I provide a program that allows to generate fake data using Statistics Canada Master files, which are available through Nesstar. The program generates (random) variables with the same name and labels as the confidential files. Those fake datasets can be used to develop codes outside the RDC (debugging, performance testing...).

In order to use the code, please proceed as follows:

1. Download the Fakedata program (see links below)

2. Recover the .xml file of the wanted survey on Nesstar (e.g. http://nesstar.library.ubc.ca/webview/)

"Statistics Canada metadata for Master Files (RDC)

<Survey/Year/Cycle of you choice>​

"Metadata"

"Other Documentation"

<survey IMDB>

Click on the "download" button (floppy disk on the upper-right corner of the screen)

Select "In xml format" Download

3. (Optional) Recover the .csv for the Public Use Microdata file (PUMF) of the corresponding survey (e.g. through ODESI)

4. Run the Fakedata program. The code will  ask for the .xml and .csv (if PUMF is provided). It will produce a .csv file of fake data as well as a .do file (Stata script) which contains the labels. To use those files, simply import the .csv in Stata and run the .do file.

