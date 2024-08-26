function PRMStat = convertSEPToPRMStat(detObj)
    numObjects = detObj.numObj;
    
    minR = 1e20;
    minRIdx = -1;
    RCP = 0;
    VCP = 0;
    NCP = 0;
    CPW = 0;
    RCF = 0;
    VCF = 0;
    NCF = 0;
    CFW = 0;
    REC = 0;
    VEC = 0;
    NEC = 0;
    ECW = 0;
    for i = 1:numObjects
        R = sqrt(detObj.x(i)^2 + detObj.y(i)^2 + detObj.z(i)^2);
        if R < minR
            minR = R;
            minRIdx = i;
        end

        snr = double(detObj.snr);
        snr = snr - mean(snr);

        NEC = NEC + 1;
        REC = REC + R * exp(snr(i));
        VEC = VEC + detObj.doppler(i) * exp(snr(i));
        ECW = ECW + exp(snr(i));

        if detObj.doppler(i) > 0
            NCP = NCP + 1;
            RCP = RCP + R * exp(snr(i));
            VCP = VCP + detObj.doppler(i) * exp(snr(i));
            CPW = CPW + exp(snr(i));
        end

        if detObj.doppler(i) <= 0
            NCF = NCF + 1;
            RCF = RCF + R * exp(snr(i));
            VCF = VCF + detObj.doppler(i) * exp(snr(i));
            CFW = CFW + exp(snr(i));
        end

    end
    
    if ECW == 0
        REC = 0;
        VEC = 0;
    else
        REC = REC / ECW;
        VEC = VEC / ECW;
    end
    
    if CPW == 0
        RCP = 0;
        VCP = 0;
    else
        RCP = RCP / CPW;
        VCP = VCP / CPW;
    end
    
    if CFW == 0
        RCF = 0;
        VCF = 0;
    else
        RCF = RCF / CFW;
        VCF = VCF / CFW;
    end


    nearest_alpha = atan(detObj.y(minRIdx)/detObj.x(minRIdx));

    PRMStat = [NEC, REC, VEC, NCP, RCP, VCP, NCF, RCF, VCF, nearest_alpha];
    
end