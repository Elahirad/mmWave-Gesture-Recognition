function model = loadTensorflowModelFromFile(filename)

    net = importNetworkFromTensorFlow(filename);
    layer = imageInputLayer([20 10 1], Normalization = "none");

    model = addInputLayer(net, layer, Initialize = true);
end
