/****************************************************************
Collect and send All Poppy Sensors data
Call and Response (Handshaking) Method
******************************************************************/

const int sampleWindow = 50; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample_mik1, sample_mik2;
int analogPin_mik1 = 0;
int analogPin_mik2 = 1;


void setup() 
{
   Serial.begin(115200);
   establishContact();
}

void loop() 
{ 
    double volts_mik[2];
	
   // collect data from Sensors
   if (Serial.available() > 0) 
    {
	  // wait Go for send data
      int inByte = Serial.read();

      Sampling_Miks(volts_mik); 	  // Mik Sensors
	    
    // Send Sensor's data to serial  
    Serial.print(volts_mik[0]);
    Serial.print(',');
    Serial.print(volts_mik[1]);
    Serial.print("\n");
	}
}


void Sampling_Miks(double *volts)
{
   unsigned long startMillis= millis();  // Start of sample window
   
   unsigned int peakToPeak_mik1 = 0;   // peak-to-peak level Mik 1
   unsigned int peakToPeak_mik2 = 0;   // peak-to-peak level Mik 2
   
   unsigned int signalMax_mik1 = 0;
   unsigned int signalMin_mik1 = 1024;
   
   unsigned int signalMax_mik2 = 0;
   unsigned int signalMin_mik2 = 1024; 

   
   while (millis() - startMillis < sampleWindow)
    {
        //Read datas from Sensors
        sample_mik1 = analogRead(analogPin_mik1);
        sample_mik2 = analogRead(analogPin_mik2);

	    if (sample_mik1 < 1024)  // toss out spurious readings
         {
	       if (sample_mik1 > signalMax_mik1)
		    {
		      signalMax_mik1 = sample_mik1;  // save just the max levels
		    }
           else if (sample_mik1 < signalMin_mik1)
		   {
		      signalMin_mik1 = sample_mik1;  // save just the min levels
		    }
         }

        if (sample_mik2 < 1024)  // toss out spurious readings
         {
	       if (sample_mik2 > signalMax_mik2)
            {
              signalMax_mik2 = sample_mik2;  // save just the max levels      		
            }
           else if (sample_mik2 < signalMin_mik2)
	        {
 	          signalMin_mik2 = sample_mik2;  // save just the min levels
	        }
         }
     }

    peakToPeak_mik1 = signalMax_mik1 - signalMin_mik1;  // max - min = peak-peak amplitude
    //volts[0] = (peakToPeak_mik1 * 3.3) / 1024;  // convert to volts 
    volts[0] = peakToPeak_mik1;
      
    peakToPeak_mik2 = signalMax_mik2 - signalMin_mik2;  // max - min = peak-peak amplitude
    //volts[1] = (peakToPeak_mik2 * 3.3) / 1024;  // convert to volts 
    volts[1] = peakToPeak_mik2;
}

void establishContact() 
{
 while (!Serial.available()) 
   {
      Serial.println("hello");   // send a starting message
      delay(300);
   }
}
