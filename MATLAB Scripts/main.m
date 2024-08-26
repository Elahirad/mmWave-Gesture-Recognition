% Clear environment and close figures
clearvars; close all;
delete(instrfind);

% Setup ports
uart_port = 'COM6';
data_port = 'COM5';
configFile = "config.cfg";

% Ask user for recording mode
recordingMode = input('Enter 1 for timed recording, 2 for manual stop: ');

% Define recording duration or setup manual stop
switch recordingMode
    case 1
        recordTime = input('Enter the recording duration in seconds: ');
    case 2
        H = uicontrol('Style', 'PushButton', ...
                      'String', 'Stop', ...
                      'Callback', 'stopVal = 1', 'Position', [100 600 100 30]);
        stopVal = 0;
end

% Setup radar and get configuration parameters
[DATA_sphandle, UART_sphandle] = radarSetup(configFile, uart_port, data_port);

% Main data reading loop
myInd = 1;
frame = {};
frame_num = {};
tic;
while true
    [dataOk, frameNumber, detObj] = readAndParseData(DATA_sphandle);
    
    if dataOk
        frame{myInd} = detObj;
        frame_num{myInd} = frameNumber;
        saveDetectedObjects(frameNumber, detObj, 'detected_objects.csv');
        myInd = myInd + 1;
    end

    if recordingMode == 1 && toc >= recordTime
        break;
    elseif recordingMode == 2 && stopVal
        break;
    end
end

% Clean up and close connections
cleanupRadar(UART_sphandle, DATA_sphandle);
