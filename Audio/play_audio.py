% MATLAB code M-file to read and view the output of the analog 
% mic reads from the arduino. 

% Open file for reading and read it.
filename = './filename.dat';
fID = fopen(filename);
MicVals = fscanf(fID, '%f',[1,inf]);
MicVals = MicVals';
fclose(fID);

Nsamp = size(MicVals,1)

% End time in milliseconds, approximately .3 milliseconds per sample.
Tend = .3*Nsamp;

time = linspace(0,Tend,Nsamp);

figure(1); clf;
plot(time,MicVals,'-k');
axis([0 Tend 400 1023]);
xlabel('\fontsize{16}milliseconds');
ylabel('\fontsize{16}Digital MIC Read');
title('\fontsize{16}Recording: No Jumps');
saveas(1,'./filename.eps','psc2');

UpSample = zeros(2*Nsamp,1);
UpSample(1:2:(2*Nsamp-1)) = MicVals;
UpSample(2:2:(2*Nsamp)) = MicVals;

% Sampling rate
Fs = 8192/(1.5); 

% Play back the audio
soundsc(UpSample,Fs)

% Write to *.wav file
% First scale data 
AudMed = median(UpSample);
AudScaled = UpSample - AudMed;
AudDev = max(abs(AudScaled));
AudScaled = AudScaled/AudDev;   wavwrite(AudScaled,Fs,'./filename.wav');
