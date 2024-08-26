function [DATA_sphandle, UART_sphandle] = radarSetup(configfile, uart_port, data_port)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%         CONFIGURE SERIAL PORT          %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% UART COM PORT:
UART_sphandle = serialport(uart_port, 115200);
configureTerminator(UART_sphandle, 'LF');
flush(UART_sphandle);

%%%% DATA COM PORT:
DATA_sphandle = serialport(data_port, 921600);
set(DATA_sphandle, 'Timeout', 10);
set(DATA_sphandle, 'InputBufferSize', 65536);
DATA_sphandle.ErrorOccurredFcn = @dispError;
% If you need to configure a specific callback function:
configureCallback(DATA_sphandle, 'byte', 2^16+1, @readUartCallbackFcn);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%        READ CONFIGURATION FILE         %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

config = cell(1,100);
fid = fopen(configfile, 'r');
if fid == -1
    fprintf('File %s not found!\n', configfile);
    return;
else
    fprintf('Opening configuration file %s ...\n', configfile);
end
tline = fgetl(fid);
k = 1;
while ischar(tline)
    config{k} = tline;
    tline = fgetl(fid);
    k = k + 1;
end
config = config(1:k-1);
fclose(fid);

%%%%%%%%%%       PARSE THE CONFIGURATION FILE         %%%%%%%%%%%
% Parsing logic remains the same
% (Ensure to include the parsing logic here)

%%%%%%%%%%        SEND CONFIGURATION TO SENSOR         %%%%%%%%%%%
mmwDemoCliPrompt = char('mmwDemo:/>');
fprintf('Sending configuration from %s file to IWR16xx ...\n', configfile);
for k = 1:length(config)
    command = config{k};
    writeline(UART_sphandle, command);
    fprintf('%s\n', command);
    echo = readline(UART_sphandle); % Get an echo of a command
    done = readline(UART_sphandle); % Get "Done"
    % prompt might need adjustment based on actual data received
end

end
