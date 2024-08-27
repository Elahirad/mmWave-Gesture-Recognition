% Clear environment and close figures
clearvars; close all;
delete(instrfind);

% Setup ports
uart_port = 'COM6';
data_port = 'COM5';
configFile = "config.cfg";

model = loadTensorflowModelFromFile('model');

% Setup radar and get configuration parameters
[DATA_sphandle, UART_sphandle] = radarSetup(configFile, uart_port, data_port);

% Initialize PRM sliding window
prmWindow = cell(1, 20); % Cell array to store up to 20 PRM statistics

handles.stopbutton = uicontrol('style', 'toggle', 'String', 'STOP', 'Value', 0);

% Main data reading loop
tic;
started = 0;

while true
    drawnow();
    quitthis = get(handles.stopbutton, 'Value');

    if quitthis
        break;
    end

    [frameNumber, detObj] = readAndParseData(DATA_sphandle);

    % Compute PRM statistics for current frame
    PRMStat = convertSEPToPRMStat(detObj);
    % savePRMToFile(PRMStat, 'prm.csv');

    % Update sliding window with shift-register behavior
    prmWindow = [prmWindow(2:end), {PRMStat}]; % Shift left and add new PRMStat at the end

    % Check if window is full and perform PS and PT
    if all(~cellfun(@isempty, prmWindow))

        prmMatrix = zeros(20, 10, 1);

        for i = 1:20
            prmMatrix(i, :, 1) = cell2mat(prmWindow(1, i));
        end

        if ~started

            if predictionStarter(prmMatrix, 5, 150, 5)
                started = 1;
                disp('Gesture started');
            end

        else

            if predictionTerminator(prmMatrix)
                started = 0;
                disp('Gesture ended');
            end

        end

        if started
            % disp("Predicting ...");
            % result = model.predict(prmMatrix);
            % res = find(result == max(result));
            % switch res
            %     case 0
            %         disp("Knock");
            %     case 1
            %         disp("Left Swipe");
            %     case 2
            %         disp("Rotate");
            %     case 3
            %         disp("Right Swipe");
            %     otherwise
            %         disp("Unexpected");
            % end
            % disp(result);
        end

    end

end

% Clean up and close connections
cleanupRadar(UART_sphandle, DATA_sphandle);
