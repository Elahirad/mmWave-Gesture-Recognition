function savePRMToFile(PRMStat, filename)

    if exist(filename, 'file')
        fid = fopen(filename, 'a'); % Append data
    else
        fid = fopen(filename, 'w'); % Create new file and write header
        fprintf(fid, 'NEC, REC, VEC, NCP, RCP, VCP, NCF, RCF, VCF, nearest_alpha\n');
    end

    fprintf(fid, '%d, %.6f, %.6f, %d, %.6f, %.6f, %d, %.6f, %.6f, %.6f\n', ...
        PRMStat(1), PRMStat(2), PRMStat(3), PRMStat(4), ...
        PRMStat(5), PRMStat(6), PRMStat(7), PRMStat(8), ...
        PRMStat(9), PRMStat(10));

end
