function hasEnded = predictionTerminator(prm)
    dopplers = prm(end - 4:end, 3);

    diffs = abs(diff(dopplers));

    threshold = 0.5;
    hasEnded = sum(diffs) >= threshold;
end
