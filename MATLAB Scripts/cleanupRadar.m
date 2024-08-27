function cleanupRadar(UART_sphandle, DATA_sphandle)
    fprintf(UART_sphandle, 'sensorStop');
    fclose(UART_sphandle);
    fclose(DATA_sphandle);
    delete(instrfind);
    close all;
end
