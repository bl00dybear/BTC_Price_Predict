def predict_probability(model, x_sample):
    return model.predict(x_sample.reshape(1, x_sample.shape[0], x_sample.shape[1]))[0][0]