def train_model(model, X_train, y_train, X_test, y_test, epochs=20, batch_size=32):
    """Antrenează modelul LSTM"""
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
    return history