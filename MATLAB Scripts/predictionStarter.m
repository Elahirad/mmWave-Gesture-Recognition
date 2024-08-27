function isGesture = predictionStarter(prm, TKi, TKa, TL)
    K = 0.5 * (sum(prm(:, 4, 1) .* (prm(:, 6, 1) .^ 2)) + sum(prm(:, 7, 1) .* (prm(:, 9, 1) .^ 2)));

    VCPS = sum(prm(:, 6, 1));
    NCPS = sum(prm(:, 4, 1));

    if NCPS == 0
        LCP = 0;
    else
        LCP = VCPS / NCPS;
    end

    VCFS = sum(prm(:, 9, 1));
    NCFS = sum(prm(:, 7, 1));

    if NCFS == 0
        LCF = 0;
    else
        LCF = VCFS / NCFS;
    end

    maxAlpha = max(prm(:, 10, 1));
    minAlpha = min(prm(:, 10, 1));

    L = (LCP + LCF) / (maxAlpha - minAlpha);

    % Check conditions
    isGesture = (K >= TKi && K <= TKa) && (L <= TL);
end
