# Airline Operations Analytics

## Project Overview
This project is about analyzing data from the U.S Bureau of Transportation Statistics regarding approximately 632,000 flights in July 2026. Using Python and libraries such as pandas, NumPy, Matplotlib, I investigated patterns in airline delays. I performed cancellation analysis, airline performance comparisons, route-level delay rates, and departure time analysis. 

## Project Objective
The objective of this project was to identify and analyze operational performance among airlines. This included investigating factors associated with the departure delay. After evaluating an overall airline performance, I examined Jetblue and Southwest shared routes, focusing on departure-delay rates by their departure period. Additionally, an airline could use this information to identify potential opertional weaknesses and leading further investigations before allocating resources. 

## Dataset Description
The dataset from the Bureau of Transportations Statistics contains 631,970 flights with 15 columns from July 2026. Each row showcases airline identifiers with their routes, delays, cancellations, departure times, arrival delays, and diversions. My analysis focuses on operational performance within July, evaluating airline reliability and differences. 

## Data Auditing and Cleaning Decisions

### Missing Departure Delays
I chose not to replace missing values with a zero but rather preserve them as it may lead to bias within results. I also found that all missing departure-delay values occurred on cancelled flights. With replacing missing values and decreasing the average departure delay we may interpret and conclude the wrong business decision such as an airline's operational side is improving when it could be the opposite. 

### Missing Arrivals Delays
During my data audit, I found 19,932 missing arrival delays, I choose not to replace them with zero because as stated in my missing departures, it may lead to unncessary bias. Upon my investigation, I also dove into cancelled and diverted flights because missing arrival-delay may be linked due to flights not reaching their destinations rather than errors.

### Duplicate Records 
During my data audit, I identified 2,366 duplicate rows. Now I retained them rather than deleting them due to the dataest not including a complete flight date. Therefore, identical flights could actually repressent separate flights operatig on different dates. If I choose to remove them without verifiying, it could have led to a reducting in the number of valid observations and again introduce bias. 

### Key Findings 
Investigating Jetblue and Southwest on the route MCO-SJU, I found Southwest conains a higher departure delay rate compared to Jetblue. On flights scheduled at 3pm or after, Southwest had a 73.55% delay while Jetblue only had a 46.67% delay rate, showcasing a difference of 26.88%. Now when I adjusted for Southwest's departure time disbution I found Jetblue was still significantly lower at 35.58%, well below Southwest's 51.03%. This suggests and warrants an investigation into what causes this mass delay among southwest flights. Could there be weather issues past 3pm or taxi times become elongated past 3pom?

## Business Recommendations
Some specific actions I woudld take if I was Southwest is investigate environment changes, airport congestion, and which aircraft is supposed to be scheduled for those flights during or after 3pm. I would also compare Southwest's delay rate with other airlines operating from MCO to determine whether the pattern is the airport-wide or airline-specific. If the investigation is to proceed and an afternoon departure leads to operational deffeciency, then Southwest should examine whether to move some flights to the morning. Now, profitability, revenue and operational impacts may need to be considered before being hasty.

## Project Limitations
One of the limitations I encountered is the dataset I have chosen is only one month out of the 12 months in a year. The month July also tends to be a high travel month for passengers. Another limitation I encountered was how limited the information regarded the causes of departure delays. The dataset does include cancellation codes but it doesn't give us the whole picture. Additionally, I don't believe delay rates necessarily mean an airline is operationally bad because there may be factors outside the airline's control which may put them at an disadvantage. 

## Tools and Tecnologies
- Python
- pandas
- NumPy
- Matplotlib
- Statistical analysis and data visualization

## Running the Project 
1. Clone or download this repository.
2. Install the required Python libraries using pip install -r requirements.txt.
3. Obtain the source dataset and place it in the data/raw/directory.
4. Ensure the outputs/figures/directory exists. 
5. Run the analysis using python data_audit.py. 