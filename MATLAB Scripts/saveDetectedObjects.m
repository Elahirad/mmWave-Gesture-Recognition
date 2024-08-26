function saveDetectedObjects(frameNumber, detObj, filename)
    % Number of detected objects in the current frame
    numObjects = detObj.numObj;

    % Open or create file, with the appropriate permissions
    if exist(filename, 'file')
        fid = fopen(filename, 'a'); % Append data
    else
        fid = fopen(filename, 'w'); % Create new file and write header
        fprintf(fid, 'Frame #, Obj #, X, Y, Z, Doppler, SNR, Noise\n');
    end

    % Iterate through each object and write data with specified format
    for i = 1:numObjects
        fprintf(fid, '%d, %d, %.3f, %.3f, %.3f, %.3f, %d, %d\n', ...
            frameNumber, i, detObj.x(i), detObj.y(i), detObj.z(i), ...
            detObj.doppler(i), detObj.snr(i), detObj.noise(i));
    end

    % Close the file
    fclose(fid);
end
