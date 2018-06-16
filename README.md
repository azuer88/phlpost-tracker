track.py
========

**track.py** displays tracking information from phlpost and description.  The tracking numbers and descriptions are stored in _data.txt_:

```
$ cat data.txt
RK999999999CN 510 Connector x 5
RF888888888SG PCB from jclpcb.com
RM777777777CN Shell for Tester
UC666666666CN SS316l wire roll
RY555555555CN ups/charger modules
LP444444444SG gprs a6 module x 2
RF333333333SG lemo 3 rta base x 5

$ ./track.py
RK999999999CN  510 Connector x 5                        6/4/2018 9:55:04 AM 
          35:   Enroute to delivery office

R8888888888SG  PCB from jclpcb.com                      6/12/2018 7:46:32 AM
          35:   Enroute to delivery office

RY555555555CN  ups/charger modules                      6/16/2018 9:43:44 AM
        1107:   Turnover to next office

RM777777777CN  Shell for Tester                         6/15/2018 9:59:00 AM
           1:   Posting of item

RF333333333SG  lemo 3 rta base x 5                                          
           0:  Not Found

LP444444444SG  gprs a6 module x 2                                           
           0:  Not Found

UC666666666CN  SS316l wire roll                                             
           0:  Not Found

$ 
 ```


 ## Version 
 * Version 0.9

 ## Contact
 #### Blue Cuenca
 * e-mail: blue.cuenca@gmail.com
