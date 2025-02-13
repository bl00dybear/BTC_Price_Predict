from model_config import MODEL_PATH

def train_model(model, X_train, y_train, X_test, y_test,interval,date,w_size, epochs=20, batch_size=32):
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))

    model_path = MODEL_PATH+interval+"_"+date+'_'+str(w_size)+"wsize.keras"
    model.save(model_path)
    return history