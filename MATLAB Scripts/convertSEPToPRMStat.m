function PRMStat = convertSEPToPRMStat(detObj)
    numObjects = detObj.numObj;

    minR = 1e20;
    minRIdx = -1;
    nearestAlpha = 0;
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
        R = sqrt(detObj.x(i) ^ 2 + detObj.y(i) ^ 2 + detObj.z(i) ^ 2);

        if R < minR
            minR = R;
            minRIdx = i;
        end

        NEC = NEC + 1;
        REC = REC + R * detObj.snr(i);
        VEC = VEC + detObj.doppler(i) * detObj.snr(i);
        ECW = ECW + detObj.snr(i);

        if detObj.doppler(i) > 0
            NCP = NCP + 1;
            RCP = RCP + R * detObj.snr(i);
            VCP = VCP + detObj.doppler(i) * detObj.snr(i);
            CPW = CPW + detObj.snr(i);
        end

        if detObj.doppler(i) <= 0
            NCF = NCF + 1;
            RCF = RCF + R * detObj.snr(i);
            VCF = VCF + detObj.doppler(i) * detObj.snr(i);
            CFW = CFW + detObj.snr(i);
        end

    end

    if ECW ~= 0
        REC = REC / ECW;
        VEC = VEC / ECW;
    end

    if CPW ~= 0
        RCP = RCP / CPW;
        VCP = VCP / CPW;
    end

    if CFW ~= 0
        RCF = RCF / CFW;
        VCF = VCF / CFW;
    end

    if minRIdx >= 0
        nearestAlpha = atan(detObj.y(minRIdx) / detObj.x(minRIdx));
    end

    fprintf("NEC=%d, REC=%.4f, VEC=%.4f, NCP=%d, RCP=%.4f, VCP=%.4f, NCF=%d, RCF=%.4f, VCF=%.4f, al=%.3f\n", NEC, REC, VEC, NCP, RCP, VCP, NCF, RCF, VCF, nearest_alpha);

    PRMStat = [NEC, REC, VEC, NCP, RCP, VCP, NCF, RCF, VCF, nearestAlpha];

end
